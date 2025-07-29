import gc
import logging
import multiprocessing
from multiprocessing.synchronize import Event
import os
import signal
import sys
from threading import Thread
import time
from time import sleep

from workflow_server.config import MEMORY_LIMIT_MB
from workflow_server.utils.exit_handler import process_killed_switch

logger = logging.getLogger(__name__)

_oom_killed_switch = multiprocessing.Event()

_MAX_MEMORY_PERCENT = 0.97
_WARN_MEMORY_PERCENT = 0.90
_FORCE_GC_MEMORY_PERCENT = 0.75
_FORCE_COLLECT_MEMORY_PERCENT = 0.90
_ACTIVE_PROCESS_COUNT = multiprocessing.Value("i", 0)
_ACTIVE_PROCESS_LOCK = multiprocessing.Lock()
_KILL_GRACE_PERIOD = 5


def increment_process_count(change: int) -> None:
    result = _ACTIVE_PROCESS_LOCK.acquire(timeout=5)
    try:
        if result:
            global _ACTIVE_PROCESS_COUNT
            _ACTIVE_PROCESS_COUNT.value += change  # type: ignore
        else:
            logger.error("Failed to lock workflow server process count global.")
    finally:
        if result:
            _ACTIVE_PROCESS_LOCK.release()


def get_active_process_count() -> int:
    return _ACTIVE_PROCESS_COUNT.value  # type: ignore


def start_oom_killer_worker() -> None:
    logger.info("Starting oom killer watcher...")
    OomKillerThread(kill_switch=_oom_killed_switch).start()


def get_is_oom_killed() -> bool:
    return _oom_killed_switch.is_set()


class OomKillerThread(Thread):
    """
    This worker is for watching for oom errors so we can gracefully kill any workflows in flight
    and tell the user they have a memory limit problem instead of relying on kubernetes to do it
    for us. This currently goes off the max memory not the requested memory so it may not always
    be accurate since max memory may not always be available
    """

    _kill_switch: Event

    def __init__(
        self,
        kill_switch: Event,
    ) -> None:
        Thread.__init__(self)
        self._kill_switch = kill_switch

    def run(self) -> None:
        last_gc = time.time()

        logger.info("Starting oom watcher...")
        if not MEMORY_LIMIT_MB:
            return

        while True:
            if process_killed_switch.is_set():
                exit(1)
            sleep(1)
            try:
                with open("/sys/fs/cgroup/memory/memory.usage_in_bytes", "r") as file:
                    memory_bytes = file.read()
            except Exception:
                logger.error("Unable to get current memory.")
                return

            if not memory_bytes:
                logger.error("Unable to get current memory.")
                return

            memory_mb = int(memory_bytes) / 1024 / 1024

            if memory_mb > (MEMORY_LIMIT_MB * _MAX_MEMORY_PERCENT):
                self._kill_switch.set()
                logger.error(
                    f"Workflow server OOM killed, memory: {memory_mb}MB, Process Count: {get_active_process_count()}"
                )
                # Give time for the threads to get our kill switch
                sleep(_KILL_GRACE_PERIOD)
                pid = os.getpid()
                os.kill(pid, signal.SIGKILL)
                sys.exit(1)

            if memory_mb > (MEMORY_LIMIT_MB * _WARN_MEMORY_PERCENT):
                logger.warning(
                    f"Memory usage exceeded 90% of limit, memory: {memory_mb}MB, "
                    f"Process Count: {get_active_process_count()}"
                )

            if memory_mb > (MEMORY_LIMIT_MB * _FORCE_GC_MEMORY_PERCENT):
                if time.time() - last_gc >= 20:
                    logger.info("Forcing garbage collect from memory pressure")
                    gc.collect()
