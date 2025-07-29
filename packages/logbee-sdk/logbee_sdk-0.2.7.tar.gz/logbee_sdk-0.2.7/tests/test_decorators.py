"""
Tests para los decoradores del SDK de Logbee.
"""
import unittest
from unittest.mock import patch
import sys
import os
from src.decorators import catch_and_log_errors
# Añadir el directorio src al path para importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))




class TestDecorators(unittest.TestCase):
    """
    Test the catch_and_log_errors decorator.
    """
    @patch('src.decorators.send_error_to_logbee')
    def test_catch_and_log_errors(self, mock_send_error):
        """Prueba el decorador catch_and_log_errors"""
        # Configurar el mock
        mock_send_error.return_value = True

        # Decorar una función que lanza una excepción
        @catch_and_log_errors(
            service_name="test-service",
            environment="test",
            client_id="test-client-id",
            client_secret="test-client-secret",
            timeout=15,
            custom_context={"test_key": "test_value"}
        )
        def function_with_error():
            raise ValueError("Test error")

        # Ejecutar la función y esperar que se capture la excepción
        with self.assertRaises(ValueError):
            function_with_error()

        # Verificar que se llamó a send_error_to_logbee
        mock_send_error.assert_called_once()

        # Verificar los argumentos pasados a send_error_to_logbee
        args, kwargs = mock_send_error.call_args

        # Verificar que se pasó la excepción correcta
        self.assertIsInstance(kwargs['error'], ValueError)
        self.assertEqual(str(kwargs['error']), "Test error")

        # Verificar el contexto
        context = kwargs['context']
        self.assertEqual(context["service_name"], "test-service")
        self.assertEqual(context["environment"], "test")
        self.assertEqual(context["test_key"], "test_value")
        self.assertEqual(context["function"], "function_with_error")

        # Verificar los parámetros de autenticación
        self.assertEqual(kwargs["client_id"], "test-client-id")
        self.assertEqual(kwargs["client_secret"], "test-client-secret")
        self.assertEqual(kwargs["timeout"], 15)


if __name__ == '__main__':
    unittest.main()
