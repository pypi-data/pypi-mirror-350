"""
This file contains the FastAPI adapter for the logging system.
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .core import build_log_data, log_to_console
from .models import ClientInfo
from .utils import generate_request_id, now_iso

class LogbeeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, options: dict):
        super().__init__(app)
        self.options = options

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        request_id = request.headers.get("X-Request-ID") or generate_request_id()

        try:
            body = await request.json()
        except Exception:
            body = None

        response: Response = await call_next(request)
        duration = round((time.perf_counter() - start_time) * 1000, 2)

        raw_data = {
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration": duration,
            "timestamp": now_iso(),
            "request_id": request_id,
            "headers": dict(request.headers),
            "body": body,
            "query": dict(request.query_params),
            "params": request.path_params,
            "client_info": ClientInfo(
                ip=request.client.host if request.client else None,
                user_agent=request.headers.get("User-Agent"),
                referer=request.headers.get("Referer"),
            )
        }

        log = build_log_data(raw_data, self.options)
        log_to_console(log)

        return response


def init_logbee(app, options: dict):
    app.add_middleware(LogbeeMiddleware, options=options)
