"""Custom exceptions for the pixoo-py library."""


class PixooError(Exception):
    """Base exception for all pixoo-py errors."""
    pass


class PixooConnectionError(PixooError):
    """Raised when there are connection issues with the device."""
    pass


class PixooCommandError(PixooError):
    """Raised when a command fails to execute on the device."""
    pass
