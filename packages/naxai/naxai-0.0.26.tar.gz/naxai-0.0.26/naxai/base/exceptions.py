"""
Exception classes for the Naxai SDK.

This module defines the exception hierarchy used throughout the SDK
to provide consistent error handling and reporting.
"""

from typing import Optional, Any

class NaxaiException(Exception):
    """Base exception for all Naxai SDK errors."""
    def __init__(self, message: str,
                 status_code: Optional[int] = None,
                 error_code: Optional[str] = None,
                 details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details

    def __str__(self):
        return (f"{self.__class__.__name__}: {self.message} "
                f"(status_code={self.status_code}, error_code={self.error_code})")

class NaxaiAuthenticationError(NaxaiException):
    """ Naxai authentication error """

class NaxaiAuthorizationError(NaxaiException):
    """ Naxai authorization error """

class NaxaiResourceNotFound(NaxaiException):
    """ Naxai resource not found error """

class NaxaiRateLimitExceeded(NaxaiException):
    """ Naxai rate limit exceeded error """

class NaxaiAPIRequestError(NaxaiException):
    """ Naxai API request error """

class NaxaiValueError(NaxaiException):
    """ Naxai value error """

class NaxaiInvalidRequestError(NaxaiException):
    """ Naxai invalid request error """
