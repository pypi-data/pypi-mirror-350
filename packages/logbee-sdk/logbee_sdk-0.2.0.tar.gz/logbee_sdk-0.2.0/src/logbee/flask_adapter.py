"""
Flask adapter for the Logbee SDK.
"""
import time
from flask import request, g
from .core import build_log_data, log_to_console, send_log_to_api, send_error_to_logbee, generate_request_id
from .models import ClientInfo

def init_logbee(app, client_id: str, client_secret: str, **options):
    """
    Initialize the Logbee SDK for Flask.

    Args:
        app: Flask application instance
        client_id: Logbee client ID (required)
        client_secret: Logbee client secret (required)
        **options: Additional configuration options including:
            - timeout: Request timeout in seconds (default: 30)
            - retry_attempts: Number of retry attempts (default: 3)
            - retry_delay: Delay between retries in seconds (default: 1.0)
            - send_to_api: Whether to send logs to API (default: True)
            - environment: Environment name
            - service_name: Service name
            - And all other SDK options...
    """
    if not client_id or not client_secret:
        raise ValueError("client_id and client_secret are required")

    # Merge client credentials with options
    full_options = {
        "client_id": client_id,
        "client_secret": client_secret,
        **options
    }

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

        log = build_log_data(raw_data, full_options)
        log_to_console(log)

        # Send to API if enabled
        if full_options.get("send_to_api", True):
            send_log_to_api(
                log,
                client_id=full_options.get("client_id"),
                client_secret=full_options.get("client_secret"),
                timeout=full_options.get("timeout", 30),
                retry_attempts=full_options.get("retry_attempts", 3),
                retry_delay=full_options.get("retry_delay", 1.0)
            )

        return response

    @app.errorhandler(Exception)
    def handle_exception(error):
        """
        Captura automáticamente TODAS las excepciones y las envía a Logbee.
        """
        # Calcular duración si tenemos start_time
        duration = None
        if hasattr(g, 'start_time'):
            duration = round((time.perf_counter() - g.start_time) * 1000, 2)

        # Preparar contexto del error
        error_context = {
            "method": request.method,
            "path": request.path,
            "status": 500,  # Error interno
            "duration": duration,
            "service_name": full_options.get("service_name"),
            "environment": full_options.get("environment"),
            "custom": {
                "user_agent": request.headers.get("User-Agent"),
                "ip": request.remote_addr,
                "request_id": g.get("request_id"),
                "headers": dict(request.headers),
                "body": request.get_json(silent=True),
                "query": request.args.to_dict(),
                "params": request.view_args,
            }
        }

        # Enviar error a Logbee automáticamente
        if full_options.get("send_to_api", True):
            send_error_to_logbee(
                error=error,
                context=error_context,
                client_id=full_options.get("client_id"),
                client_secret=full_options.get("client_secret"),
                timeout=full_options.get("timeout", 30),
                retry_attempts=full_options.get("retry_attempts", 3),
                retry_delay=full_options.get("retry_delay", 1.0)
            )

        # Re-lanzar la excepción para que Flask la maneje normalmente
        raise error
