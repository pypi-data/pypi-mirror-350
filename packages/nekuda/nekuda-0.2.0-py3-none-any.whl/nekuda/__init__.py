"""
Nekuda SDK - Python client for Nekuda payment processing API
"""

from .client import NekudaClient
from .exceptions import (
    NekudaError,
    NekudaApiError,
    NekudaConnectionError,
    NekudaValidationError,
    AuthenticationError,
    InvalidRequestError,
    CardNotFoundError,
    RateLimitError,
    ServerError,
)
from ._globals import get_default_client, set_default_client

__version__ = "0.2.0"
__all__ = [
    "NekudaClient",
    "NekudaError",
    "NekudaApiError",
    "NekudaConnectionError",
    "NekudaValidationError",
    "UserContext",
    "MandateData",
    "CardDetails",
    "AuthenticationError",
    "InvalidRequestError",
    "CardNotFoundError",
    "RateLimitError",
    "ServerError",
    "get_default_client",
    "set_default_client",
]

# Convenience re-exports for IDEs
from .user import UserContext  # noqa: E402 – re-export placed after __all__
from .models import MandateData, CardDetails
