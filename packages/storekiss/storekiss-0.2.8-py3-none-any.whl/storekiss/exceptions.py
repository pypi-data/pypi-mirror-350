"""
Custom exceptions for the storekiss library.
"""


class StorekissError(Exception):
    """Base exception for all storekiss errors."""

    pass


class ValidationError(StorekissError):
    """Raised when data validation fails."""

    pass


class NotFoundError(StorekissError):
    """Raised when a requested item is not found."""

    pass


class DatabaseError(StorekissError):
    """Raised when there's an error with the database operations."""

    pass
