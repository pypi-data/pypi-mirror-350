"""
Decorators to simplify integration with Logbee.
"""
import functools
from typing import Any, Dict, Optional
from .core import send_error_to_logbee

def catch_and_log_errors(
    service_name: Optional[str] = None,
    environment: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    timeout: int = 30,
    custom_context: Optional[Dict[str, Any]] = None
):
    """
    Decorator that captures exceptions in a function and sends them automatically to Logbee.

    Args:
        service_name: Service name (optional)
        environment: Application environment (optional)
        client_id: Client ID for authentication with Logbee (optional)
        client_secret: Client secret for authentication with Logbee (optional)
        timeout: Request timeout in seconds (default: 30)
        custom_context: Additional context information (optional)

    Returns:
        The configured decorator

    Usage example:
        @catch_and_log_errors(service_name="my-service", environment="production", client_id="your-client-id", client_secret="your-client-secret")
        def some_function():
            # If an exception occurs here, it will be captured and sent to Logbee
            raise ValueError("This error will be captured and sent to Logbee")
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Prepare the context
                context = {}
                if custom_context:
                    context.update(custom_context)

                if service_name:
                    context["service_name"] = service_name
                if environment:
                    context["environment"] = environment

                # Add information about the function
                context["function"] = func.__name__
                context["module"] = func.__module__

                # Send error to Logbee
                send_error_to_logbee(
                    error=e,
                    context=context,
                    client_id=client_id,
                    client_secret=client_secret,
                    timeout=timeout
                )

                # Re-raise the exception to not interfere with normal flow
                raise

        return wrapper
    return decorator
