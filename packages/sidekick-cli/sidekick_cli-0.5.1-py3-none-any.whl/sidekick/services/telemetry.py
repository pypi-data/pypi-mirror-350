"""
Module: sidekick.services.telemetry

Provides telemetry and error tracking functionality using Sentry.
Manages Sentry SDK initialization and event callbacks.
"""

import os
from typing import Any, Callable, Dict, List, Optional

import sentry_sdk

from sidekick.core.state import StateManager


def _create_before_send_callback(
    state_manager: StateManager,
) -> Callable[[Dict[str, Any], Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Create a before_send callback with access to state_manager."""

    def _before_send(event: Dict[str, Any], hint: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Filter sensitive data from Sentry events."""
        if not state_manager.session.telemetry_enabled:
            return None

        if event.get("request") and event["request"].get("headers"):
            headers = event["request"]["headers"]
            for key in list(headers.keys()):
                if key.lower() in ("authorization", "cookie", "x-api-key"):
                    headers[key] = "[Filtered]"

        if event.get("extra") and event["extra"].get("sys.argv"):
            args: List[str] = event["extra"]["sys.argv"]
            for i, arg in enumerate(args):
                if "key" in arg.lower() or "token" in arg.lower() or "secret" in arg.lower():
                    args[i] = "[Filtered]"

        if event.get("extra") and event["extra"].get("message"):
            event["extra"]["message"] = "[Content Filtered]"

        return event

    return _before_send


def setup(state_manager: StateManager) -> None:
    """Setup Sentry for error reporting if telemetry is enabled."""
    if not state_manager.session.telemetry_enabled:
        return

    IS_DEV = os.environ.get("IS_DEV", False) == "True"
    environment = "development" if IS_DEV else "production"

    sentry_sdk.init(
        dsn="https://c967e1bebffe899093ed6bc2ee2e90c7@o171515.ingest.us.sentry.io/4509084774105088",
        traces_sample_rate=0.1,  # Sample only 10% of transactions
        profiles_sample_rate=0.1,  # Sample only 10% of profiles
        send_default_pii=False,  # Don't send personally identifiable information
        before_send=_create_before_send_callback(state_manager),  # Filter sensitive data
        environment=environment,
        debug=False,
        shutdown_timeout=0,
    )

    sentry_sdk.set_user(
        {"id": state_manager.session.device_id, "session_id": state_manager.session.session_id}
    )


def capture_exception(*args: Any, **kwargs: Any) -> Optional[str]:
    return sentry_sdk.capture_exception(*args, **kwargs)
