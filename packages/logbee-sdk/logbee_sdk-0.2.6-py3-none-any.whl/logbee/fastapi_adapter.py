"""
This file contains the FastAPI adapter for the logging system.
"""

import time
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .core import build_log_data, log_to_console, send_log_to_api, send_error_to_logbee
from .models import ClientInfo
from .utils import generate_request_id, now_iso

class LogbeeMiddleware(BaseHTTPMiddleware):
    """
    Middleware for FastAPI to log requests and responses.
    """
    def __init__(self, app, client_id: str, client_secret: str, **options):
        """
        Initialize the middleware.

        Args:
            app: FastAPI application instance
            client_id: Logbee client ID (required)
            client_secret: Logbee client secret (required)
            **options: Additional configuration options
        """
        super().__init__(app)
        if not client_id or not client_secret:
            raise ValueError("client_id and client_secret are required")

        self.options = {
            "client_id": client_id,
            "client_secret": client_secret,
            **options
        }

    async def dispatch(self, request: Request, call_next):
        """
        Dispatch the request.
        """
        start_time = time.perf_counter()
        request_id = request.headers.get("X-Request-ID") or generate_request_id()

        # Mejorar el manejo del body para evitar cadenas vacías
        body = None
        try:
            # Intentar leer el body como bytes primero
            body_bytes = await request.body()
            if body_bytes:
                try:
                    # Si hay contenido, intentar parsear como JSON
                    body_str = body_bytes.decode('utf-8')
                    if body_str.strip():  # Solo si no es cadena vacía o solo espacios
                        body = json.loads(body_str)
                    else:
                        body = None
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Si no es JSON válido o hay error de decodificación, usar None
                    body = None
            else:
                body = None
        except Exception:
            body = None

        try:
            # Procesar la request normalmente
            response: Response = await call_next(request)
            duration = int(round((time.perf_counter() - start_time) * 1000))

            # Log de request exitosa o con error HTTP
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

            # Send to API if enabled
            if self.options.get("send_to_api", True):
                result = send_log_to_api(
                    log,
                    client_id=self.options.get("client_id"),
                    client_secret=self.options.get("client_secret"),
                    timeout=self.options.get("timeout", 30),
                    retry_attempts=self.options.get("retry_attempts", 3),
                    retry_delay=self.options.get("retry_delay", 1.0)
                )

            return response

        except Exception as error:
            # Captura automática de TODAS las excepciones
            duration = int(round((time.perf_counter() - start_time) * 1000))

            # Preparar contexto del error
            error_context = {
                "method": request.method,
                "path": request.url.path,
                "status": 500,  # Error interno
                "duration": duration,
                "service_name": self.options.get("service_name"),
                "environment": self.options.get("environment"),
                "custom": {
                    "user_agent": request.headers.get("User-Agent"),
                    "ip": request.client.host if request.client else None,
                    "request_id": request_id,
                    "headers": dict(request.headers),
                    "body": body,
                    "query": dict(request.query_params),
                    "params": request.path_params,
                }
            }

            # Enviar error a Logbee automáticamente
            if self.options.get("send_to_api", True):
                result = send_error_to_logbee(
                    error=error,
                    context=error_context,
                    client_id=self.options.get("client_id"),
                    client_secret=self.options.get("client_secret"),
                    timeout=self.options.get("timeout", 30),
                    retry_attempts=self.options.get("retry_attempts", 3),
                    retry_delay=self.options.get("retry_delay", 1.0)
                )

            # Re-lanzar la excepción para que FastAPI la maneje normalmente
            raise error


def init_logbee(app, client_id: str, client_secret: str, **options):
    """
    Initialize the Logbee SDK for FastAPI.

    Args:
        app: FastAPI application instance
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
    app.add_middleware(LogbeeMiddleware, client_id=client_id, client_secret=client_secret, **options)
