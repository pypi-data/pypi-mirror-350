"""
This file contains the initialization of the logging system.
"""
__version__ = "0.2.6"

# Core imports (always available)
from .models import LogData, ErrorData
from .core import build_log_data, log_to_console, send_log_to_api, send_error_to_logbee
from .config import LOGBEE_API_ENDPOINT, DEFAULT_OPTIONS
from .decorators import catch_and_log_errors

# Optional imports for framework adapters
try:
    from .flask_adapter import init_logbee as init_logbee_flask
except ImportError:
    init_logbee_flask = None

try:
    from .fastapi_adapter import init_logbee as init_logbee_fastapi
except ImportError:
    init_logbee_fastapi = None

try:
    from .django_middleware import LogbeeMiddleware as LogbeeDjangoMiddleware
except ImportError:
    LogbeeDjangoMiddleware = None

__all__ = [
    "LogData",
    "ErrorData",
    "build_log_data",
    "log_to_console",
    "send_log_to_api",
    "send_error_to_logbee",
    "catch_and_log_errors",
    "LOGBEE_API_ENDPOINT",
    "DEFAULT_OPTIONS",
]

# Add optional imports to __all__ if available
if init_logbee_flask is not None:
    __all__.append("init_logbee_flask")
if init_logbee_fastapi is not None:
    __all__.append("init_logbee_fastapi")
if LogbeeDjangoMiddleware is not None:
    __all__.append("LogbeeDjangoMiddleware")
