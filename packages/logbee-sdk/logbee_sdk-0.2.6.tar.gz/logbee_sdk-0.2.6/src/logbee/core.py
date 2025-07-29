"""
This file contains the core functionality for the logging system.
"""
import platform
import time
from datetime import datetime, timezone
from dataclasses import asdict
import traceback
from typing import Any, Dict, List, Optional
import json
import logging
import requests


from .models import LogData, ErrorData, ClientInfo
from .utils import generate_request_id
from .config import LOGBEE_API_ENDPOINT

logger = logging.getLogger("logbee")


def snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.split('_')
    return components[0] + ''.join(word.capitalize() for word in components[1:])


def convert_dict_to_camel_case(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert dictionary keys from snake_case to camelCase recursively."""
    if not isinstance(data, dict):
        return data

    converted = {}
    for key, value in data.items():
        # Convert the key to camelCase
        camel_key = snake_to_camel(key)

        # Recursively convert nested dictionaries
        if isinstance(value, dict):
            converted[camel_key] = convert_dict_to_camel_case(value)
        elif isinstance(value, list):
            # Handle lists that might contain dictionaries
            converted[camel_key] = [
                convert_dict_to_camel_case(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            converted[camel_key] = value

    return converted


def sanitize_data(data: Any, sensitive_fields: Optional[List[str]]) -> Any:
    """
    Sanitize data by replacing sensitive fields with "[REDACTED]".
    """
    if not sensitive_fields or not isinstance(data, dict):
        return data
    return {
        key: ("[REDACTED]" if key in sensitive_fields else value)
        for key, value in data.items()
    }

def build_log_data(
    raw_data: Dict[str, Any],
    options: Dict[str, Any]
) -> LogData:
    """
    Build a LogData object from raw data.
    """
    # Check if we should capture this request based on status code
    status_code = raw_data.get("status", 200)
    min_status_code = options.get("min_status_code_to_capture", 0)
    capture_all_requests = options.get("capture_all_requests", True)

    # If capture_all_requests is False and status code is below minimum, skip detailed capture
    should_capture_details = capture_all_requests or status_code >= min_status_code

    # Process body only if we should capture details
    body = None
    if should_capture_details and options.get("capture_body", True):
        body = raw_data.get("body")
        if options.get("mask_sensitive_data", True) and body:
            body = sanitize_data(body, options.get("sensitive_fields", []))

    return LogData(
        method=raw_data.get("method", "UNKNOWN"),
        path=raw_data.get("path", ""),
        status=status_code,
        duration=raw_data.get("duration"),
        timestamp=raw_data.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        request_id=raw_data.get("request_id") or generate_request_id(),
        body=body,
        headers=raw_data.get("headers") if (options.get("capture_headers", True) and should_capture_details) else None,
        query=raw_data.get("query") if (options.get("capture_query_params", True) and should_capture_details) else None,
        params=raw_data.get("params"),
        client_info=raw_data.get("client_info"),
        environment=options.get("environment"),
        service_name=options.get("service_name"),
        error=raw_data.get("error"),
        custom=raw_data.get("custom"),
    )

def log_to_console(log: LogData):
    """
    Log to console.
    """
    # This is just for debugging, later you could log to a file or send it
    logger.info(f"[{log.timestamp}] {log.method} {log.path} ({log.status}) - {log.duration}ms")

def send_log_to_api(log_data: LogData, client_id: str, client_secret: str, timeout: int = 30, retry_attempts: int = 3, retry_delay: float = 1.0) -> bool:
    """
    Send log data to the Logbee API.
    """
    # Convert LogData to dictionary
    data = {
        "method": log_data.method,
        "path": log_data.path,
        "status": log_data.status,
        "duration": log_data.duration,
        "timestamp": log_data.timestamp,
        "request_id": log_data.request_id,
        "body": log_data.body,
        "headers": log_data.headers,
        "query": log_data.query,
        "params": log_data.params,
        "client_info": {
            "ip": log_data.client_info.ip if log_data.client_info else None,
            "user_agent": log_data.client_info.user_agent if log_data.client_info else None,
            "referer": log_data.client_info.referer if log_data.client_info else None,
        } if log_data.client_info else None,
        "environment": log_data.environment,
        "service_name": log_data.service_name,
        "error": {
            "message": log_data.error.message,
            "stack": log_data.error.stack,
            "code": log_data.error.code,
            "name": log_data.error.name,
        } if log_data.error else None,
        "custom": log_data.custom,
    }

    # Convert to camelCase
    camel_case_data = convert_dict_to_camel_case(data)

    # Filter out None values to clean the payload
    def remove_none_values(obj):
        if isinstance(obj, dict):
            return {k: remove_none_values(v) for k, v in obj.items() if v is not None and v != ""}
        elif isinstance(obj, list):
            return [remove_none_values(item) for item in obj if item is not None and item != ""]
        else:
            return obj

    camel_case_data = remove_none_values(camel_case_data)

    url = LOGBEE_API_ENDPOINT
    headers = {
        "Content-Type": "application/json",
        "clientId": client_id,
        "clientSecret": client_secret,
    }

    for attempt in range(retry_attempts):
        try:
            response = requests.post(url, json=camel_case_data, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return True
            else:
                print(f"Error sending log to Logbee API. Status: {response.status_code}, Response: {response.text}")
        except requests.RequestException as e:
            print(f"Request exception: {e}")

        if attempt < retry_attempts - 1:
            time.sleep(retry_delay)

    return False

def send_error_to_logbee(error: Exception, context: Dict[str, Any] = None, client_id: str = None, client_secret: str = None, timeout: int = 30, retry_attempts: int = 3, retry_delay: float = 1.0):
    """
    Specific function to send captured errors to the Logbee API.

    Args:
        error: The captured exception
        context: Additional information about the context where the error occurred
        client_id: Client ID for authentication with the Logbee service
        client_secret: Client secret for authentication with the Logbee service
        timeout: Request timeout in seconds (default: 30)
        retry_attempts: Number of retry attempts (default: 3)
        retry_delay: Delay between retries in seconds (default: 1.0)

    Returns:
        bool: True if the send was successful, False otherwise
    """
    # Create error data
    error_data = ErrorData(
        message=str(error),
        name=error.__class__.__name__,
        stack=getattr(error, "__traceback__", None) and ''.join(
            traceback.format_exception(type(error), error, error.__traceback__)
        ),
        code=getattr(error, "code", None) or getattr(error, "status_code", None)
    )

    # Create a LogData object with the minimum required information
    timestamp = datetime.now(timezone.utc).isoformat()
    request_id = generate_request_id()

    context = context or {}
    method = context.get("method", "ERROR")
    path = context.get("path", f"/error/{error.__class__.__name__}")

    # Crear ClientInfo a partir del contexto si está disponible
    client_info = None
    if any(key in context for key in ['ip_address', 'user_agent', 'referer']):
        client_info = ClientInfo(
            ip=context.get('ip_address'),
            user_agent=context.get('user_agent'),
            referer=context.get('referer')
        )

    log_data = LogData(
        method=method,
        path=path,
        status=context.get("status", 500),
        timestamp=timestamp,
        request_id=request_id,
        error=error_data,
        service_name=context.get("service_name", "python-app"),
        environment=context.get("environment", "development"),
        custom=context.get("custom"),
        client_info=client_info
    )

    # Send to API
    return send_log_to_api(log_data, client_id=client_id, client_secret=client_secret, timeout=timeout, retry_attempts=retry_attempts, retry_delay=retry_delay)
