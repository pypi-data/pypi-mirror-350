"""
Utility functions for the Logbee SDK.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, List, Optional


def generate_request_id() -> str:
    """
    Generate a unique request ID.
    """
    return str(uuid.uuid4())


def now_iso() -> str:
    """
    Get the current time in ISO format.
    """
    return datetime.now(timezone.utc).isoformat()


def sanitize_data(data: Any, sensitive_fields: Optional[List[str]]) -> Any:
    """
    Sanitize data by replacing sensitive fields with "[REDACTED]".
    """
    if not sensitive_fields or not isinstance(data, dict):
        return data
    sanitized = {}
    for key, value in data.items():
        if key in sensitive_fields:
            sanitized[key] = "[REDACTED]"
        else:
            sanitized[key] = value
    return sanitized
