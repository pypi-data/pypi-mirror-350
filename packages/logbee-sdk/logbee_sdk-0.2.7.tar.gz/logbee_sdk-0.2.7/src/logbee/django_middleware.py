"""
Django middleware for the Logbee SDK.
"""
import time
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from .core import build_log_data, log_to_console, send_log_to_api
from .models import ClientInfo
from .utils import generate_request_id, now_iso

class LogbeeMiddleware(MiddlewareMixin):
    """
    Middleware for Django to log requests and responses.
    """
    # Atributo requerido para Django 5.x
    async_mode = False

    def __init__(self, get_response=None):
        """
        Initialize the middleware.
        """
        self.get_response = get_response
        # Obtener opciones desde settings de Django
        self.options = getattr(settings, 'LOGBEE_OPTIONS', {})

    def process_request(self, request):
        """
        Process the request.
        """
        request._logbee_start_time = time.perf_counter()
        request._logbee_request_id = request.headers.get("X-Request-ID") or generate_request_id()

    def process_response(self, request, response):
        """
        Process the response.
        """
        duration = None
        if hasattr(request, '_logbee_start_time'):
            duration = int(round((time.perf_counter() - request._logbee_start_time) * 1000))

        try:
            body_str = request.body.decode('utf-8')
            if body_str:
                try:
                    # Intentar parsear como JSON
                    import json
                    body = json.loads(body_str)
                except json.JSONDecodeError:
                    # Si no es JSON válido, usar None en lugar de cadena
                    body = None
            else:
                body = None
        except Exception:
            body = None

        raw_data = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration": duration,
            "timestamp": now_iso(),
            "request_id": getattr(request, '_logbee_request_id', None),
            "headers": dict(request.headers),
            "body": body,
            "query": request.GET.dict(),
            "params": getattr(request, 'resolver_match', None) and request.resolver_match.kwargs,
            "client_info": ClientInfo(
                ip=request.META.get("REMOTE_ADDR"),
                user_agent=request.headers.get("User-Agent"),
                referer=request.headers.get("Referer"),
            )
        }

        log = build_log_data(raw_data, self.options)

        # Only process and send the log if it should be captured
        if log is not None:
            log_to_console(log)

            # Send to API if enabled
            if self.options.get("send_to_api", True):
                try:
                    result = send_log_to_api(
                        log,
                        client_id=self.options.get("client_id"),
                        client_secret=self.options.get("client_secret"),
                        timeout=self.options.get("timeout", 30),
                        retry_attempts=self.options.get("retry_attempts", 3),
                        retry_delay=self.options.get("retry_delay", 1.0)
                    )
                except Exception as e:
                    import traceback
                    traceback.print_exc()

        return response
