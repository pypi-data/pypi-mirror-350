import time
from django.utils.deprecation import MiddlewareMixin
from .core import build_log_data, log_to_console
from .models import ClientInfo
from .utils import generate_request_id, now_iso

class LogbeeMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None, **options):
        self.get_response = get_response
        self.options = options

    def process_request(self, request):
        request._logbee_start_time = time.perf_counter()
        request._logbee_request_id = request.headers.get("X-Request-ID") or generate_request_id()

    def process_response(self, request, response):
        duration = None
        if hasattr(request, '_logbee_start_time'):
            duration = round((time.perf_counter() - request._logbee_start_time) * 1000, 2)

        try:
            body = request.body.decode('utf-8')
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
        log_to_console(log)

        return response
