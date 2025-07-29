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


from .models import LogData, ErrorData
from .utils import generate_request_id
from .config import LOGBEE_API_ENDPOINT

logger = logging.getLogger("logbee")


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

def send_log_to_api(log: LogData, client_id: str = None, client_secret: str = None, timeout: int = 30, retry_attempts: int = 3, retry_delay: float = 1.0):
    """
    Sends log data to the Logbee API.

    Args:
        log: LogData object with the information to send
        client_id: Client ID for authentication with the Logbee service
        client_secret: Client secret for authentication with the Logbee service
        timeout: Request timeout in seconds (default: 30)
        retry_attempts: Number of retry attempts (default: 3)
        retry_delay: Delay between retries in seconds (default: 1.0)

    Returns:
        bool: True if the send was successful, False otherwise
    """
    for attempt in range(retry_attempts + 1):
        try:
            # Convert the LogData object to a dictionary
            log_dict = asdict(log)

            # Filter None fields to reduce payload size
            log_dict = {k: v for k, v in log_dict.items() if v is not None}

            # Prepare JSON data
            data = json.dumps(log_dict)

            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "Content-Length": str(len(data.encode('utf-8'))),
                "User-Agent": f"LogbeeHttpMonitor/Python-{platform.python_version()}",
            }

            # Add authentication headers if provided
            if client_id:
                headers["clientId"] = client_id
            if client_secret:
                headers["clientSecret"] = client_secret

            response = requests.post(
                LOGBEE_API_ENDPOINT,
                headers=headers,
                data=data,
                timeout=timeout
            )

            if response.status_code >= 200 and response.status_code < 300:
                logger.debug(f"Log sent successfully to Logbee API. Request ID: {log.request_id}")
                return True
            else:
                logger.error(f"Error sending log to Logbee API. Status: {response.status_code}, Response: {response.text}")
                if attempt < retry_attempts:
                    logger.info(f"Retrying in {retry_delay} seconds... (attempt {attempt + 1}/{retry_attempts})")
                    time.sleep(retry_delay)
                    continue
                return False

        except requests.exceptions.Timeout:
            logger.error(f"Request timeout after {timeout}s when sending log to Logbee API")
            if attempt < retry_attempts:
                logger.info(f"Retrying in {retry_delay} seconds... (attempt {attempt + 1}/{retry_attempts})")
                time.sleep(retry_delay)
                continue
            return False
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error when sending log to Logbee API: {str(e)}")
            if attempt < retry_attempts:
                logger.info(f"Retrying in {retry_delay} seconds... (attempt {attempt + 1}/{retry_attempts})")
                time.sleep(retry_delay)
                continue
            return False
        except Exception as e:
            logger.exception(f"Exception when sending log to Logbee API: {str(e)}")
            if attempt < retry_attempts:
                logger.info(f"Retrying in {retry_delay} seconds... (attempt {attempt + 1}/{retry_attempts})")
                time.sleep(retry_delay)
                continue
            return False

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

    log_data = LogData(
        method=method,
        path=path,
        status=context.get("status", 500),
        timestamp=timestamp,
        request_id=request_id,
        error=error_data,
        service_name=context.get("service_name", "python-app"),
        environment=context.get("environment", "development"),
        custom=context.get("custom")
    )

    # Send to API
    return send_log_to_api(log_data, client_id=client_id, client_secret=client_secret, timeout=timeout, retry_attempts=retry_attempts, retry_delay=retry_delay)
