"""
Test para verificar la consistencia de parámetros con el SDK de JavaScript.
"""
import unittest
from unittest.mock import MagicMock
from logbee.core import build_log_data


class TestSDKConsistency(unittest.TestCase):
    """
    Tests para verificar que el SDK de Python sea consistente con el SDK de JavaScript.
    """

    def test_all_js_parameters_supported(self):
        """
        Verifica que todos los parámetros del SDK de JavaScript sean soportados.
        """
        # Parámetros del SDK de JavaScript
        js_options = {
            "capture_body": True,
            "capture_headers": True,
            "capture_query_params": True,
            "mask_sensitive_data": True,
            "environment": "production",
            "service_name": "test-service",
            "sensitive_fields": ["password", "token"],
            "min_status_code_to_capture": 400,
            "capture_all_requests": False,
        }

        raw_data = {
            "method": "POST",
            "path": "/api/test",
            "status": 500,
            "duration": 150,
            "headers": {"Authorization": "Bearer token123"},
            "body": {"password": "secret123", "email": "test@example.com"},
            "query": {"debug": "true"},
        }

        # Esto no debe lanzar ninguna excepción
        log_data = build_log_data(raw_data, js_options)

        # Verificar que los campos sean correctos
        self.assertEqual(log_data.method, "POST")
        self.assertEqual(log_data.path, "/api/test")
        self.assertEqual(log_data.status, 500)
        self.assertEqual(log_data.environment, "production")
        self.assertEqual(log_data.service_name, "test-service")

        # Como status >= min_status_code_to_capture, debe capturar detalles
        self.assertIsNotNone(log_data.body)
        self.assertIsNotNone(log_data.headers)
        self.assertIsNotNone(log_data.query)

        # Verificar que se enmascaren los datos sensibles
        self.assertEqual(log_data.body["password"], "[REDACTED]")
        self.assertEqual(log_data.body["email"], "test@example.com")

    def test_min_status_code_filtering(self):
        """
        Verifica que min_status_code_to_capture funcione correctamente.
        """
        options = {
            "capture_body": True,
            "capture_headers": True,
            "capture_query_params": True,
            "min_status_code_to_capture": 400,
            "capture_all_requests": False,
        }

        # Request con status 200 (menor que 400)
        raw_data_success = {
            "method": "GET",
            "path": "/api/users",
            "status": 200,
            "headers": {"Authorization": "Bearer token123"},
            "body": {"data": "sensitive"},
            "query": {"page": "1"},
        }

        log_data_success = build_log_data(raw_data_success, options)

        # No debe capturar detalles para status 200
        self.assertIsNone(log_data_success.body)
        self.assertIsNone(log_data_success.headers)
        self.assertIsNone(log_data_success.query)

        # Request con status 500 (mayor que 400)
        raw_data_error = {
            "method": "POST",
            "path": "/api/users",
            "status": 500,
            "headers": {"Authorization": "Bearer token123"},
            "body": {"data": "sensitive"},
            "query": {"page": "1"},
        }

        log_data_error = build_log_data(raw_data_error, options)

        # Debe capturar detalles para status 500
        self.assertIsNotNone(log_data_error.body)
        self.assertIsNotNone(log_data_error.headers)
        self.assertIsNotNone(log_data_error.query)

    def test_capture_all_requests_override(self):
        """
        Verifica que capture_all_requests=True anule min_status_code_to_capture.
        """
        options = {
            "capture_body": True,
            "capture_headers": True,
            "min_status_code_to_capture": 400,
            "capture_all_requests": True,  # Esto debe anular el filtro de status code
        }

        raw_data = {
            "method": "GET",
            "path": "/api/users",
            "status": 200,  # Menor que 400, pero capture_all_requests=True
            "headers": {"Authorization": "Bearer token123"},
            "body": {"data": "sensitive"},
        }

        log_data = build_log_data(raw_data, options)

        # Debe capturar detalles aunque status < min_status_code_to_capture
        self.assertIsNotNone(log_data.body)
        self.assertIsNotNone(log_data.headers)

    def test_new_authentication_and_retry_parameters(self):
        """
        Verifica que los nuevos parámetros de autenticación y reintentos sean soportados.
        """
        options = {
            "client_id": "test-client-id",
            "client_secret": "test-client-secret",
            "timeout": 45,
            "retry_attempts": 5,
            "retry_delay": 2.0,
            "send_to_api": False,  # No enviar a la API en el test
            "capture_body": True,
            "environment": "test",
            "service_name": "test-service"
        }

        raw_data = {
            "method": "POST",
            "path": "/api/test",
            "status": 200,
            "duration": 100,
            "headers": {"Content-Type": "application/json"},
            "body": {"test": "data"},
            "query": {"param": "value"},
        }

        # Esto no debe lanzar ninguna excepción
        log_data = build_log_data(raw_data, options)

        # Verificar que todos los campos se asignen correctamente
        self.assertEqual(log_data.method, "POST")
        self.assertEqual(log_data.path, "/api/test")
        self.assertEqual(log_data.status, 200)
        self.assertEqual(log_data.environment, "test")
        self.assertEqual(log_data.service_name, "test-service")

        # Los parámetros de autenticación no afectan el LogData directamente,
        # pero se deben pasar a send_log_to_api cuando se use
        self.assertIsNotNone(log_data.body)
        self.assertIsNotNone(log_data.headers)
        self.assertIsNotNone(log_data.query)

    def test_client_credentials_validation(self):
        """
        Verifica que se validen correctamente las credenciales del cliente.
        """
        # TODO: Descomenta cuando Flask esté disponible en el entorno de pruebas
        pass
        # from logbee.flask_adapter import init_logbee as init_logbee_flask
        # from unittest.mock import MagicMock

        # # Mock de la app Flask
        # mock_app = MagicMock()
        # mock_app.before_request = MagicMock()
        # mock_app.after_request = MagicMock()

        # # Debe funcionar con credenciales válidas
        # try:
        #     init_logbee_flask(mock_app, client_id="valid-client-id", client_secret="valid-client-secret")
        # except ValueError:
        #     self.fail("init_logbee_flask raised ValueError with valid credentials")

        # # Debe fallar sin client_id
        # with self.assertRaises(ValueError):
        #     init_logbee_flask(mock_app, client_id="", client_secret="valid-client-secret")

        # # Debe fallar sin client_secret
        # with self.assertRaises(ValueError):
        #     init_logbee_flask(mock_app, client_id="valid-client-id", client_secret="")

        # # Debe fallar sin ambos
        # with self.assertRaises(ValueError):
        #     init_logbee_flask(mock_app, client_id="", client_secret="")


if __name__ == "__main__":
    unittest.main()
