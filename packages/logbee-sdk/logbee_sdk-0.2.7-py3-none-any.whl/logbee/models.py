"""
This file contains the models for the logging system.
"""
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class ClientInfo:
    """
    Client information.
    """
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    referer: Optional[str] = None

@dataclass
class ErrorData:
    """
    Error data.
    """
    message: str
    stack: Optional[str] = None
    code: Optional[str] = None
    name: Optional[str] = None

@dataclass
class LogData:
    """
    Log data.
    """
    method: str
    path: str
    status: Optional[int] = None
    duration: Optional[float] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_id: Optional[str] = None
    body: Optional[Any] = None
    headers: Optional[Dict[str, Any]] = None
    query: Optional[Dict[str, Any]] = None
    params: Optional[Dict[str, str]] = None
    client_info: Optional[ClientInfo] = None
    environment: Optional[str] = None
    service_name: Optional[str] = None
    error: Optional[ErrorData] = None
    custom: Optional[Dict[str, Any]] = None
