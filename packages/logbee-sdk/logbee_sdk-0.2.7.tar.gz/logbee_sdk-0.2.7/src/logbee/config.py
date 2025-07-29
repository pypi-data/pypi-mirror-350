"""
Configuration file for the Logbee SDK.
"""

# API endpoint configuration
LOGBEE_API_ENDPOINT = "https://api.logbee.dev/api/v1/logs"

# Default options
DEFAULT_OPTIONS = {
    "capture_body": True,
    "capture_headers": True,
    "capture_query_params": True,
    "mask_sensitive_data": True,
    "sensitive_fields": ["password", "token", "secret", "credit_card", "card_number"],
    "environment": "development",
    "service_name": "python-app",
    "timeout": 30,  # Request timeout in seconds
}
