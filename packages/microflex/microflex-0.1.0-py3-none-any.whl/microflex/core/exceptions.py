"""
Custom exceptions for the microflex library.

This module defines all custom exceptions used throughout the microflex library
to provide clear error handling and debugging information.
"""

from typing import Optional, Any


class MicroflexError(Exception):
    """Base exception class for all microflex-related errors."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Return string representation of the exception."""
        if self.details:
            return f"{self.message}. Details: {self.details}"
        return self.message


class ValidationError(MicroflexError):
    """Raised when input validation fails."""

    pass


class ProcessingError(MicroflexError):
    """Raised when data processing fails."""

    pass


class ClassificationError(MicroflexError):
    """Raised when taxonomic classification fails."""

    pass


class IOError(MicroflexError):
    """Raised when input/output operations fail."""

    pass


class ConfigurationError(MicroflexError):
    """Raised when configuration is invalid or missing."""

    pass


class DependencyError(MicroflexError):
    """Raised when required external dependencies are missing."""

    pass


class AnalysisError(MicroflexError):
    """Raised when analysis operations fail."""

    pass


class VisualizationError(MicroflexError):
    """Raised when visualization operations fail."""

    pass 