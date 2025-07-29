"""
Voyado Engage Python Client Library

A Python client for interacting with the Voyado Engage API v3.
"""

from .client import VoyadoClient
from .exceptions import (
    VoyadoError,
    VoyadoAPIError,
    VoyadoAuthenticationError,
    VoyadoRateLimitError,
    VoyadoValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "VoyadoClient",
    "VoyadoError",
    "VoyadoAPIError",
    "VoyadoAuthenticationError",
    "VoyadoRateLimitError",
    "VoyadoValidationError",
]
