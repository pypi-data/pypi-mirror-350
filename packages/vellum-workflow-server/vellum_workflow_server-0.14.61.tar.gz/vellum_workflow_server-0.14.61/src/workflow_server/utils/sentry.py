import logging
from typing import Optional

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


def before_send(event: dict, hint: dict) -> Optional[dict]:
    if "exc_info" in hint:
        _, _, _ = hint["exc_info"]

    return event


def init_sentry(*, sentry_log_level: Optional[int], dsn: str) -> None:
    sentry_logging = LoggingIntegration(
        level=sentry_log_level,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )
    integrations = [sentry_logging]

    sentry_sdk.init(
        dsn=dsn,
        integrations=integrations,
        environment="production",
        traces_sample_rate=0.0,
        send_default_pii=True,
        before_send=before_send,  # type: ignore
        max_request_body_size="always",
        max_value_length=10_000,
    )
