class VectorDBCloudError(Exception):
    """Base exception for all VectorDBCloud errors."""
    pass


class AuthenticationError(VectorDBCloudError):
    """Authentication error."""
    pass


class RateLimitError(VectorDBCloudError):
    """Rate limit exceeded error."""
    pass


class ResourceNotFoundError(VectorDBCloudError):
    """Resource not found error."""
    pass


class ValidationError(VectorDBCloudError):
    """Validation error."""
    pass


class ServerError(VectorDBCloudError):
    """Server error."""
    pass
