"""
Tests para las funciones core del SDK de Logbee.
"""
import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Añadir el directorio src al path para importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import LogData, ErrorData
from src.core import build_log_data, send_log_to_api, send_error_to_logbee


class TestCore(unittest.TestCase):

    def test_build_log_data(self):
        """Prueba la función build_log_data con datos básicos"""
        raw_data = {
            "method": "GET",
            "path": "/test",
            "status": 200,
            "duration": 10.5,
            "timestamp": "2023-01-01T12:00:00Z",
            "request_id": "test-id-123",
            "body": {"test": "data"}
        }

        options = {
            "capture_body": True,
            "environment": "test",
            "service_name": "test-service"
        }

        log_data = build_log_data(raw_data, options)

        self.assertEqual(log_data.method, "GET")
        self.assertEqual(log_data.path, "/test")
        self.assertEqual(log_data.status, 200)
        self.assertEqual(log_data.duration, 10.5)
        self.assertEqual(log_data.timestamp, "2023-01-01T12:00:00Z")
        self.assertEqual(log_data.request_id, "test-id-123")
        self.assertEqual(log_data.body, {"test": "data"})
        self.assertEqual(log_data.environment, "test")
        self.assertEqual(log_data.service_name, "test-service")

    @patch('src.core.requests.post')
    def test_send_log_to_api(self, mock_post):
        """Prueba el envío de logs a la API"""
        # Configurar el mock
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        # Crear un LogData básico
        log_data = LogData(
            method="GET",
            path="/test",
            status=200,
            request_id="test-id-123"
        )

        # Ejecutar la función
        result = send_log_to_api(log_data, api_key="test-key")

        # Verificar que se llamó a requests.post con los parámetros correctos
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        # Verificar la URL
        self.assertEqual(args[0], "https://api.logbee.dev/api/v1/logs")

        # Verificar los headers
        self.assertEqual(kwargs['headers']['Content-Type'], "application/json")
        self.assertEqual(kwargs['headers']['Authorization'], "Bearer test-key")

        # Verificar que el resultado es True (éxito)
        self.assertTrue(result)

    @patch('src.core.send_log_to_api')
    def test_send_error_to_logbee(self, mock_send_log):
        """Prueba el envío de errores a Logbee"""
        # Configurar el mock
        mock_send_log.return_value = True

        # Crear una excepción
        error = ValueError("Test error")

        # Contexto adicional
        context = {
            "service_name": "test-service",
            "environment": "test",
            "custom": {"test_key": "test_value"}
        }

        # Ejecutar la función
        result = send_error_to_logbee(error, context, api_key="test-key")

        # Verificar que se llamó a send_log_to_api
        mock_send_log.assert_called_once()

        # Verificar el LogData que se pasó a send_log_to_api
        args, kwargs = mock_send_log.call_args
        log_data = args[0]

        self.assertEqual(log_data.method, "ERROR")
        self.assertEqual(log_data.status, 500)
        self.assertEqual(log_data.service_name, "test-service")
        self.assertEqual(log_data.environment, "test")
        self.assertEqual(log_data.custom, {"test_key": "test_value"})
        self.assertEqual(log_data.error.message, "Test error")
        self.assertEqual(log_data.error.name, "ValueError")

        # Verificar que se pasó la api_key
        self.assertEqual(kwargs["api_key"], "test-key")

        # Verificar que el resultado es True (éxito)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
