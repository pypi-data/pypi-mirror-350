"""
Exception classes for Voyado Engage API client.
"""


class VoyadoError(Exception):
    """Base exception for Voyado API errors."""
    pass


class VoyadoAPIError(VoyadoError):
    """Exception raised for API-related errors."""
    
    def __init__(self, message, status_code=None, response_data=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class VoyadoAuthenticationError(VoyadoAPIError):
    """Exception raised for authentication errors."""
    pass


class VoyadoRateLimitError(VoyadoAPIError):
    """Exception raised when API rate limit is exceeded."""
    pass


class VoyadoValidationError(VoyadoAPIError):
    """Exception raised for validation errors."""
    pass


class VoyadoNotFoundError(VoyadoAPIError):
    """Exception raised when a resource is not found."""
    pass
