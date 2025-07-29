import time
from flask import request, g
from .core import build_log_data, log_to_console, generate_request_id
from .models import ClientInfo
from typing import Callable

def init_logbee(app, options: dict):
    @app.before_request
    def start_timer():
        g.start_time = time.perf_counter()
        g.request_id = request.headers.get("X-Request-ID") or generate_request_id()
        g.request_id_from_sdk = True

    @app.after_request
    def log_response(response):
        duration = round((time.perf_counter() - g.get("start_time", 0)) * 1000, 2)

        raw_data = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration": duration,
            "timestamp": None,  # core lo pone
            "request_id": g.get("request_id"),
            "headers": dict(request.headers),
            "body": request.get_json(silent=True),
            "query": request.args.to_dict(),
            "params": request.view_args,
            "client_info": ClientInfo(
                ip=request.remote_addr,
                user_agent=request.headers.get("User-Agent"),
                referer=request.headers.get("Referer"),
            )
        }

        log = build_log_data(raw_data, options)
        log_to_console(log)
        return response
