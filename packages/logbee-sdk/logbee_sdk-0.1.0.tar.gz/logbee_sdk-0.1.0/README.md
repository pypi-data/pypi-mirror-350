# Logbee SDK para Python

SDK oficial para integrar aplicaciones Python con Logbee, una plataforma de monitoreo y gestión de errores.

## Instalación

```bash
pip install logbee-sdk
```

### Dependencias opcionales

Para usar el SDK con frameworks específicos, puedes instalar las dependencias correspondientes:

```bash
# Para Flask
pip install logbee-sdk[flask]

# Para FastAPI
pip install logbee-sdk[fastapi]

# Para Django
pip install logbee-sdk[django]

# Para todos los frameworks
pip install logbee-sdk[all]
```

## Uso

### Integración con Flask

```python
from flask import Flask
from logbee import init_logbee_flask

app = Flask(__name__)

# Inicializar Logbee
init_logbee_flask(app, api_key="tu-api-key", environment="production")

@app.route('/')
def hello():
    return "Hello World!"
```

### Integración con FastAPI

```python
from fastapi import FastAPI
from logbee import init_logbee_fastapi

app = FastAPI()

# Inicializar Logbee
init_logbee_fastapi(app, api_key="tu-api-key", environment="production")

@app.get('/')
def hello():
    return {"message": "Hello World!"}
```

### Integración con Django

En tu archivo `settings.py`:

```python
MIDDLEWARE = [
    # ... otros middlewares
    'logbee.LogbeeDjangoMiddleware',
]

# Configuración de Logbee
LOGBEE = {
    'api_key': 'tu-api-key',
    'environment': 'production',
    'service_name': 'mi-aplicacion-django',
}
```

### Envío manual de errores

```python
from logbee import send_error_to_logbee

try:
    # Código que puede generar excepciones
    result = 1 / 0
except Exception as e:
    # Enviar error a Logbee
    send_error_to_logbee(
        error=e,
        context={
            "service_name": "mi-servicio",
            "environment": "production",
            "custom": {"operacion": "división"}
        },
        api_key="tu-api-key"
    )
    # Puedes relanzar la excepción o manejarla según tu lógica
    raise
```

### Uso del decorador para capturar errores

```python
from logbee import catch_and_log_errors

@catch_and_log_errors(
    service_name="mi-servicio",
    environment="production",
    api_key="tu-api-key"
)
def funcion_con_posibles_errores():
    # Si ocurre una excepción aquí, será enviada automáticamente a Logbee
    result = 1 / 0
    return result
```

## Opciones de configuración

El SDK de Logbee admite las siguientes opciones:

- `api_key`: Tu API key de Logbee (requerido)
- `environment`: Entorno de ejecución (ej. "development", "production")
- `service_name`: Nombre de tu servicio o aplicación
- `capture_body`: Si se debe capturar el cuerpo de las peticiones (por defecto: True)
- `capture_headers`: Si se deben capturar los headers de las peticiones (por defecto: True)
- `capture_query_params`: Si se deben capturar los parámetros de consulta (por defecto: True)
- `mask_sensitive_data`: Si se deben ocultar datos sensibles (por defecto: True)
- `sensitive_fields`: Lista de campos que deben ocultarse (por defecto: ["password", "token", "secret", "credit_card", "card_number"])

## Licencia

Este proyecto está bajo la licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
