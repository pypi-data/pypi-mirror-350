"""
VectorDBCloud SDK Exceptions
Custom exception classes for the SDK
"""

class VectorDBCloudError(Exception):
    """Base exception for VectorDBCloud SDK."""
    pass

class AuthenticationError(VectorDBCloudError):
    """Authentication related errors."""
    pass

class APIError(VectorDBCloudError):
    """API response errors."""
    pass

class ValidationError(VectorDBCloudError):
    """Input validation errors."""
    pass

class ConnectionError(VectorDBCloudError):
    """Connection related errors."""
    pass
