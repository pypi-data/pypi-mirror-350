"""Custom exceptions for Ruru CLI."""


class RuruError(Exception):
    """Base exception for all Ruru CLI errors."""

    pass


class RuruAPIError(RuruError):
    """Exception raised for API-related errors."""

    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(RuruAPIError):
    """Exception raised for authentication errors (401)."""

    pass


class NotFoundError(RuruAPIError):
    """Exception raised for not found errors (404)."""

    pass


class ValidationError(RuruAPIError):
    """Exception raised for validation errors (422)."""

    pass


class ConfigurationError(RuruError):
    """Exception raised for configuration-related errors."""

    pass


class FileOperationError(RuruError):
    """Exception raised for file operation errors."""

    pass
