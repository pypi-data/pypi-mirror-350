import uuid
from datetime import datetime, timezone
from typing import Any, List, Dict, Optional


def generate_request_id() -> str:
    return str(uuid.uuid4())


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sanitize_data(data: Any, sensitive_fields: Optional[List[str]]) -> Any:
    if not sensitive_fields or not isinstance(data, dict):
        return data
    sanitized = {}
    for key, value in data.items():
        if key in sensitive_fields:
            sanitized[key] = "[REDACTED]"
        else:
            sanitized[key] = value
    return sanitized
