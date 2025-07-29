from datetime import datetime
import importlib
from io import StringIO
import json
import logging
from multiprocessing import Process, Queue
import os
import random
import string
import sys
from threading import Event as ThreadingEvent
import time
from traceback import format_exc
from uuid import uuid4
from typing import Any, Callable, Generator, Iterator, Optional, Tuple, Type

from pebble import concurrent
from vellum_ee.workflows.display.workflows import BaseWorkflowDisplay
from vellum_ee.workflows.server.virtual_file_loader import VirtualFileFinder

from vellum import Vellum, VellumEnvironment
from vellum.workflows import BaseWorkflow
from vellum.workflows.errors import WorkflowError, WorkflowErrorCode
from vellum.workflows.events.types import BaseEvent
from vellum.workflows.events.workflow import WorkflowEventDisplayContext
from vellum.workflows.exceptions import WorkflowInitializationException
from vellum.workflows.inputs import BaseInputs
from vellum.workflows.nodes import BaseNode
from vellum.workflows.nodes.mocks import MockNodeExecution
from vellum.workflows.state.base import BaseState, StateMeta
from vellum.workflows.state.context import WorkflowContext
from vellum.workflows.state.store import EmptyStore
from vellum.workflows.workflows.event_filters import all_workflow_event_filter
from workflow_server.config import IS_VPC, VELLUM_API_URL_HOST, VELLUM_API_URL_PORT
from workflow_server.core.cancel_workflow import CancelWorkflowWatcherThread
from workflow_server.core.events import (
    STREAM_FINISHED_EVENT,
    VembdaExecutionFulfilledBody,
    VembdaExecutionFulfilledEvent,
)
from workflow_server.core.workflow_executor_context import (
    DEFAULT_TIMEOUT_SECONDS,
    BaseExecutorContext,
    NodeExecutorContext,
    WorkflowExecutorContext,
)
from workflow_server.utils.log_proxy import redirect_log

logger = logging.getLogger(__name__)


@concurrent.process(timeout=DEFAULT_TIMEOUT_SECONDS)
# type ignore since pebble annotation changes return type
def stream_node_pebble_timeout(
    executor_context: NodeExecutorContext,
    queue: Queue,
) -> None:
    _stream_node_wrapper(
        executor_context=executor_context,
        queue=queue,
    )


def _stream_node_wrapper(executor_context: NodeExecutorContext, queue: Queue) -> None:
    try:
        for event in stream_node(executor_context=executor_context):
            queue.put(event)
    except Exception as e:
        logger.exception(e)
        queue.put(
            VembdaExecutionFulfilledEvent(
                id=uuid4(),
                timestamp=datetime.now(),
                trace_id=executor_context.trace_id,
                span_id=executor_context.execution_id,
                body=VembdaExecutionFulfilledBody(
                    exit_code=-1,
                    stderr="Internal Server Error",
                    container_overhead_latency=executor_context.container_overhead_latency,
                ),
                parent=None,
            ).model_dump(mode="json")
        )


def _stream_workflow_wrapper(executor_context: WorkflowExecutorContext, queue: Queue) -> None:
    try:
        for event in stream_workflow(executor_context=executor_context):
            queue.put(json.dumps(event))

    except WorkflowInitializationException as e:
        queue.put(
            VembdaExecutionFulfilledEvent(
                id=uuid4(),
                timestamp=datetime.now(),
                trace_id=executor_context.trace_id,
                span_id=executor_context.execution_id,
                body=VembdaExecutionFulfilledBody(
                    exit_code=-1,
                    stderr=str(e),
                    container_overhead_latency=executor_context.container_overhead_latency,
                ),
                parent=None,
            ).model_dump(mode="json")
        )
    except Exception as e:
        logger.exception(e)
        queue.put(
            VembdaExecutionFulfilledEvent(
                id=uuid4(),
                timestamp=datetime.now(),
                trace_id=executor_context.trace_id,
                span_id=executor_context.execution_id,
                body=VembdaExecutionFulfilledBody(
                    exit_code=-1,
                    stderr="Internal Server Error",
                    container_overhead_latency=executor_context.container_overhead_latency,
                ),
                parent=None,
            ).model_dump(mode="json")
        )
    queue.put(STREAM_FINISHED_EVENT)

    exit(0)


def stream_workflow_process_timeout(
    executor_context: WorkflowExecutorContext,
    queue: Queue,
) -> Process:
    workflow_process = Process(
        target=_stream_workflow_wrapper,
        args=(
            executor_context,
            queue,
        ),
    )
    workflow_process.start()

    if workflow_process.exitcode is not None:
        vembda_fulfilled_event = VembdaExecutionFulfilledEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            trace_id=executor_context.trace_id,
            span_id=executor_context.execution_id,
            body=VembdaExecutionFulfilledBody(
                exit_code=-1,
                timed_out=True,
                container_overhead_latency=executor_context.container_overhead_latency,
            ),
            parent=None,
        )
        queue.put(vembda_fulfilled_event.model_dump(mode="json"))

    return workflow_process


def stream_workflow(
    executor_context: WorkflowExecutorContext,
    disable_redirect: bool = True,
) -> Iterator[dict]:
    workflow, namespace = _gather_workflow(executor_context)
    workflow_inputs = _get_workflow_inputs(executor_context)
    display_context = _gather_display_context(workflow, namespace)
    workflow_state = (
        workflow.deserialize_state(
            executor_context.state,
            workflow_inputs=workflow_inputs or BaseInputs(),
        )
        if executor_context.state
        else None
    )
    run_from_node = _get_run_from_node(executor_context, workflow)
    node_output_mocks = MockNodeExecution.validate_all(
        executor_context.node_output_mocks,
        workflow.__class__,
    )

    def call_workflow() -> Generator[dict[str, Any], Any, None]:
        cancel_watcher_kill_switch = ThreadingEvent()
        cancel_signal = ThreadingEvent()
        cancel_watcher = CancelWorkflowWatcherThread(
            kill_switch=cancel_watcher_kill_switch,
            execution_id=executor_context.execution_id,
            timeout_seconds=executor_context.timeout,
            vembda_public_url=executor_context.vembda_public_url,
            cancel_signal=cancel_signal,
        )

        try:
            if executor_context.vembda_public_url:
                cancel_watcher.start()

            stream = workflow.stream(
                inputs=workflow_inputs,
                state=workflow_state,
                node_output_mocks=node_output_mocks,
                event_filter=all_workflow_event_filter,
                cancel_signal=cancel_signal,
                entrypoint_nodes=[run_from_node] if run_from_node else None,
            )

            first = True
            for event in stream:
                if first:
                    executor_context.stream_start_time = time.time_ns()
                    first = False
                    if event.name == "workflow.execution.initiated":
                        event.body.display_context = display_context

                if event.name.endswith("rejected") and event.body.error.code.name == "INTERNAL_ERROR":  # type: ignore
                    logger.exception(event.body.error.message)  # type: ignore
                    event.body.error = WorkflowError(  # type: ignore
                        code=WorkflowErrorCode.INTERNAL_ERROR.value, message="Internal Error"  # type: ignore
                    )

                yield _dump_event(
                    event=event,
                    executor_context=executor_context,
                )
        finally:
            cancel_watcher_kill_switch.set()

    return _call_stream(
        executor_context=executor_context,
        stream_generator=call_workflow,
        disable_redirect=disable_redirect,
    )


def stream_node(
    executor_context: NodeExecutorContext,
    disable_redirect: bool = True,
) -> Iterator[dict]:
    namespace = _get_file_namespace(executor_context)

    def call_node() -> Generator[dict[str, Any], Any, None]:
        sys.meta_path.append(VirtualFileFinder(executor_context.files, namespace))
        workflow_context = _create_workflow_context(executor_context)
        node_module = importlib.import_module(f"{namespace}.{executor_context.node_module}")

        Node = getattr(node_module, executor_context.node_name)

        workflow_inputs = _get_workflow_inputs(executor_context)
        workflow_state = _get_workflow_state(executor_context, workflow_inputs=workflow_inputs)

        node = Node(
            state=workflow_state,
            context=workflow_context,
        )

        executor_context.stream_start_time = time.time_ns()
        node_outputs = node.run()

        if isinstance(node_outputs, (Iterator)):
            for node_output in node_outputs:
                yield json.loads(json.dumps(node_output, default=vars))
        else:
            yield json.loads(json.dumps(node_outputs, default=vars))

    return _call_stream(
        executor_context=executor_context,
        stream_generator=call_node,
        disable_redirect=disable_redirect,
    )


def _call_stream(
    executor_context: BaseExecutorContext,
    stream_generator: Callable[[], Generator[dict[str, Any], Any, None]],
    disable_redirect: bool = True,
) -> Iterator[dict]:
    log_redirect: Optional[StringIO] = None

    if not disable_redirect:
        log_redirect = redirect_log()

    try:
        yield from stream_generator()

        vembda_fulfilled_event = VembdaExecutionFulfilledEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            trace_id=executor_context.trace_id,
            span_id=executor_context.execution_id,
            body=VembdaExecutionFulfilledBody(
                exit_code=0,
                log=log_redirect.getvalue() if log_redirect else "",
                stderr="",
                container_overhead_latency=executor_context.container_overhead_latency,
            ),
            parent=None,
        )
        yield vembda_fulfilled_event.model_dump(mode="json")

    except Exception:
        vembda_fulfilled_event = VembdaExecutionFulfilledEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            trace_id=executor_context.trace_id,
            span_id=executor_context.execution_id,
            body=VembdaExecutionFulfilledBody(
                exit_code=-1,
                log=log_redirect.getvalue() if log_redirect else "",
                stderr=format_exc(),
                container_overhead_latency=executor_context.container_overhead_latency,
            ),
            parent=None,
        )
        yield vembda_fulfilled_event.model_dump(mode="json")


def _create_workflow(executor_context: WorkflowExecutorContext, namespace: str) -> BaseWorkflow:
    workflow_context = _create_workflow_context(executor_context)
    Workflow = BaseWorkflow.load_from_module(namespace)
    VembdaExecutionFulfilledEvent.model_rebuild(
        # Not sure why this is needed, but it is required for the VembdaExecutionFulfilledEvent to be
        # properly rebuilt with the recursive types.
        _types_namespace={
            "BaseWorkflow": BaseWorkflow,
            "BaseNode": BaseNode,
        },
    )

    return Workflow(context=workflow_context, store=EmptyStore())


def _create_workflow_context(executor_context: BaseExecutorContext) -> WorkflowContext:
    if IS_VPC:
        environment = VellumEnvironment(
            default=os.getenv("VELLUM_DEFAULT_API_URL", VellumEnvironment.PRODUCTION.default),
            documents=os.getenv("VELLUM_DOCUMENTS_API_URL", VellumEnvironment.PRODUCTION.documents),
            predict=os.getenv("VELLUM_PREDICT_API_URL", VellumEnvironment.PRODUCTION.predict),
        )
    elif os.getenv("USE_LOCAL_VELLUM_API") == "true":
        VELLUM_API_URL = f"http://{VELLUM_API_URL_HOST}:{VELLUM_API_URL_PORT}"
        environment = VellumEnvironment(
            default=VELLUM_API_URL,
            documents=VELLUM_API_URL,
            predict=VELLUM_API_URL,
        )
    else:
        environment = VellumEnvironment.PRODUCTION

    return WorkflowContext(
        vellum_client=Vellum(
            api_key=executor_context.workspace_api_key,
            environment=environment,
        ),
        execution_context=executor_context.execution_context,
        generated_files=executor_context.files,
    )


def _get_file_namespace(executor_context: BaseExecutorContext) -> str:
    return str(executor_context.execution_id) or "".join(
        random.choice(string.ascii_letters + string.digits) for i in range(14)
    )


def _dump_event(event: BaseEvent, executor_context: BaseExecutorContext) -> dict:
    module_base = executor_context.module.split(".")
    dump = event.model_dump(mode="json")
    if dump["name"] in {
        "workflow.execution.initiated",
        "workflow.execution.fulfilled",
        "workflow.execution.rejected",
        "workflow.execution.streaming",
        "workflow.execution.paused",
        "workflow.execution.resumed",
    }:
        dump["body"]["workflow_definition"]["module"] = module_base + dump["body"]["workflow_definition"]["module"][1:]
    elif dump["name"] in {
        "node.execution.initiated",
        "node.execution.fulfilled",
        "node.execution.rejected",
        "node.execution.streaming",
        "node.execution.paused",
        "node.execution.resumed",
    }:
        dump["body"]["node_definition"]["module"] = module_base + dump["body"]["node_definition"]["module"][1:]

    return dump


def _get_workflow_inputs(executor_context: BaseExecutorContext) -> Optional[BaseInputs]:
    if not executor_context.inputs:
        return None

    if not executor_context.files.get("inputs.py"):
        return None

    namespace = _get_file_namespace(executor_context)
    inputs_module_path = f"{namespace}.inputs"
    try:
        inputs_module = importlib.import_module(inputs_module_path)
    except Exception as e:
        raise WorkflowInitializationException(f"Failed to initialize workflow inputs: {e}") from e

    if not hasattr(inputs_module, "Inputs"):
        raise WorkflowInitializationException(
            f"Inputs module {inputs_module_path} does not have a required Inputs class"
        )

    if not issubclass(inputs_module.Inputs, BaseInputs):
        raise WorkflowInitializationException(
            f"""The class {inputs_module_path}.Inputs was expected to be a subclass of BaseInputs, \
but found {inputs_module.Inputs.__class__.__name__}"""
        )

    return inputs_module.Inputs(**executor_context.inputs)


def _get_workflow_state(
    executor_context: BaseExecutorContext, workflow_inputs: Optional[BaseInputs]
) -> Optional[BaseState]:
    namespace = _get_file_namespace(executor_context)
    State = importlib.import_module(f"{namespace}.state").State if executor_context.files.get("state.py") else None

    if not State:
        return None

    if not issubclass(State, BaseState):
        return None

    if executor_context.state:
        return State(**executor_context.state)

    if workflow_inputs:
        return State(
            meta=StateMeta(workflow_inputs=workflow_inputs),
        )

    return State()


def _get_run_from_node(executor_context: WorkflowExecutorContext, workflow: BaseWorkflow) -> Optional[Type[BaseNode]]:
    if not executor_context.node_id:
        return None

    for node in workflow.get_nodes():
        if node.__id__ == executor_context.node_id:
            return node

    return None


def _gather_workflow(context: WorkflowExecutorContext) -> Tuple[BaseWorkflow, str]:
    try:
        namespace = _get_file_namespace(context)
        sys.meta_path.append(VirtualFileFinder(context.files, namespace))
        workflow = _create_workflow(
            executor_context=context,
            namespace=namespace,
        )
        return workflow, namespace
    except Exception as e:
        logger.exception("Failed to initialize Workflow")
        raise WorkflowInitializationException(f"Failed to initialize workflow: {e}") from e


def _gather_display_context(workflow: BaseWorkflow, namespace: str) -> Optional["WorkflowEventDisplayContext"]:
    try:
        return BaseWorkflowDisplay.gather_event_display_context(namespace, workflow.__class__)
    except Exception:
        logger.exception("Unable to Parse Workflow Display Context")
        return None
