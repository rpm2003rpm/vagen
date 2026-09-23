"""Custom exceptions for the vagen package."""


class VagenError(Exception):
    """Base exception for vagen."""


class VagenTypeError(VagenError, TypeError):
    """Raised when an argument has the wrong type."""


class VagenValueError(VagenError, ValueError):
    """Raised when an argument has an invalid value."""


class VagenSequenceError(VagenError, RuntimeError):
    """Raised when a command is used outside a valid sequence context."""


class VagenNameError(VagenError, ValueError):
    """Raised when a name is invalid or already taken."""
