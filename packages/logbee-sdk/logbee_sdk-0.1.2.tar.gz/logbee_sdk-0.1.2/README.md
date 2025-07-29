# Logbee SDK for Python

Official SDK for integrating Python applications with Logbee, an error monitoring and logging platform.

## Installation

```bash
pip install logbee-sdk
```

### Optional dependencies

To use the SDK with specific frameworks, you can install the corresponding dependencies:

```bash
# For Flask
pip install logbee-sdk[flask]

# For FastAPI
pip install logbee-sdk[fastapi]

# For Django
pip install logbee-sdk[django]

# For all frameworks
pip install logbee-sdk[all]
```

## Usage

### Flask Integration

```python
from flask import Flask
from logbee import init_logbee_flask

app = Flask(__name__)

# Initialize Logbee
init_logbee_flask(app, client_id="your-client-id", client_secret="your-client-secret", environment="production")

@app.route('/')
def hello():
    return "Hello World!"
```

### FastAPI Integration

```python
from fastapi import FastAPI
from logbee import init_logbee_fastapi

app = FastAPI()

# Initialize Logbee
init_logbee_fastapi(app, client_id="your-client-id", client_secret="your-client-secret", environment="production")

@app.get('/')
def hello():
    return {"message": "Hello World!"}
```

### Django Integration

In your `settings.py` file:

```python
MIDDLEWARE = [
    # ... other middlewares
    'logbee.LogbeeDjangoMiddleware',
]

# Logbee configuration
LOGBEE = {
    'client_id': 'your-client-id',
    'client_secret': 'your-client-secret',
    'environment': 'production',
    'service_name': 'my-django-app',
    'timeout': 30,
}
```

### Manual error reporting

```python
from logbee import send_error_to_logbee

try:
    # Code that might raise exceptions
    result = 1 / 0
except Exception as e:
    # Send error to Logbee
    send_error_to_logbee(
        error=e,
        context={
            "service_name": "my-service",
            "environment": "production",
            "custom": {"operation": "division"}
        },
        client_id="your-client-id",
        client_secret="your-client-secret"
    )
    # You can re-raise the exception or handle it according to your logic
    raise
```

### Using the decorator to catch errors

```python
from logbee import catch_and_log_errors

@catch_and_log_errors(
    service_name="my-service",
    environment="production",
    client_id="your-client-id",
    client_secret="your-client-secret"
)
def function_with_possible_errors():
    # If an exception occurs here, it will be automatically sent to Logbee
    result = 1 / 0
    return result
```

## Configuration options

The Logbee SDK supports the following options:

- `client_id`: Your Logbee client ID (required)
- `client_secret`: Your Logbee client secret (required)
- `environment`: Runtime environment (e.g. "development", "production")
- `service_name`: Name of your service or application
- `timeout`: Request timeout in seconds (default: 30)
- `capture_body`: Whether to capture request bodies (default: True)
- `capture_headers`: Whether to capture request headers (default: True)
- `capture_query_params`: Whether to capture query parameters (default: True)
- `mask_sensitive_data`: Whether to mask sensitive data (default: True)
- `sensitive_fields`: List of fields to be masked (default: ["password", "token", "secret", "credit_card", "card_number"])

## API Reference

### Core Functions

#### `send_error_to_logbee(error, context=None, client_id=None, client_secret=None, timeout=30)`

Sends an error to the Logbee API.

**Parameters:**
- `error` (Exception): The exception to be sent
- `context` (dict, optional): Additional context information
- `client_id` (str, optional): Client ID for authentication
- `client_secret` (str, optional): Client secret for authentication
- `timeout` (int, optional): Request timeout in seconds (default: 30)

**Returns:**
- `bool`: True if successful, False otherwise

#### `send_log_to_api(log_data, client_id=None, client_secret=None, timeout=30)`

Sends log data to the Logbee API.

**Parameters:**
- `log_data` (LogData): Log data object
- `client_id` (str, optional): Client ID for authentication
- `client_secret` (str, optional): Client secret for authentication
- `timeout` (int, optional): Request timeout in seconds (default: 30)

**Returns:**
- `bool`: True if successful, False otherwise

### Decorators

#### `@catch_and_log_errors(**kwargs)`

Decorator that automatically catches and sends exceptions to Logbee.

**Parameters:**
- `service_name` (str, optional): Service name
- `environment` (str, optional): Environment name
- `client_id` (str, optional): Client ID for authentication
- `client_secret` (str, optional): Client secret for authentication
- `timeout` (int, optional): Request timeout in seconds (default: 30)
- `custom_context` (dict, optional): Additional context

## Requirements

- Python 3.7+
- requests >= 2.25.0

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
