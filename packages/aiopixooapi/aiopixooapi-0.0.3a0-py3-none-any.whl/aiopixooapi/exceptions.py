"""Custom exceptions for the pixoo-py library."""


class PixooError(Exception):
    """Base exception for all pixoo-py errors."""



class PixooConnectionError(PixooError):
    """Raised when there are connection issues with the device."""



class PixooCommandError(PixooError):
    """Raised when a command fails to execute on the device."""

