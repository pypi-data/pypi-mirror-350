"""
Base classes for the microflex library.

This module provides base implementations that can be extended by
specific components throughout the library.
"""

import time
from typing import Any, Dict, List

from microflex.core.exceptions import ValidationError, ProcessingError
from microflex.core.interfaces import Processor
from microflex.core.types import SequenceCollection, ProcessingResult


class BaseProcessor(Processor):
    """
    Base implementation of the Processor interface.

    This class provides common functionality for all processors including
    validation, timing, and result tracking.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the base processor.

        Args:
            **kwargs: Configuration parameters
        """
        super().__init__(**kwargs)
        self._input_count = 0
        self._output_count = 0
        self._filtered_count = 0
        self._processing_time = 0.0
        self._warnings: List[str] = []
        self._errors: List[str] = []

    def process(self, data: SequenceCollection) -> SequenceCollection:
        """
        Process sequence data with timing and validation.

        Args:
            data: Input sequence collection

        Returns:
            Processed sequence collection

        Raises:
            ValidationError: If input validation fails
            ProcessingError: If processing fails
        """
        # Reset statistics
        self._reset_stats()
        
        # Validate input
        if not self.validate_input(data):
            raise ValidationError("Input validation failed")

        self._input_count = len(data)
        start_time = time.time()

        try:
            # Perform the actual processing
            result = self._process_implementation(data)
            self._output_count = len(result)
            self._filtered_count = self._input_count - self._output_count

        except Exception as e:
            self._errors.append(str(e))
            raise ProcessingError(f"Processing failed: {e}") from e

        finally:
            self._processing_time = time.time() - start_time

        return result

    def _process_implementation(self, data: SequenceCollection) -> SequenceCollection:
        """
        Actual processing implementation to be overridden by subclasses.

        Args:
            data: Input sequence collection

        Returns:
            Processed sequence collection
        """
        # Default implementation returns input unchanged
        return data

    def validate_input(self, data: SequenceCollection) -> bool:
        """
        Validate input data.

        Args:
            data: Input data to validate

        Returns:
            True if data is valid, False otherwise
        """
        if not data:
            self._warnings.append("Empty input data")
            return False

        if not isinstance(data, list):
            self._errors.append("Input data must be a list")
            return False

        # Validate each sequence
        for i, seq_data in enumerate(data):
            if not hasattr(seq_data, 'sequence') or not hasattr(seq_data, 'sequence_id'):
                self._errors.append(f"Invalid sequence data at index {i}")
                return False

            if not seq_data.sequence:
                self._warnings.append(f"Empty sequence at index {i}")

            if not seq_data.sequence_id:
                self._errors.append(f"Missing sequence ID at index {i}")
                return False

        return True

    def get_processing_stats(self) -> ProcessingResult:
        """
        Get processing statistics.

        Returns:
            Processing result with statistics
        """
        return ProcessingResult(
            input_count=self._input_count,
            output_count=self._output_count,
            filtered_count=self._filtered_count,
            processing_time=self._processing_time,
            parameters=self.config.copy(),
            warnings=self._warnings.copy(),
            errors=self._errors.copy(),
        )

    def _reset_stats(self) -> None:
        """Reset processing statistics."""
        self._input_count = 0
        self._output_count = 0
        self._filtered_count = 0
        self._processing_time = 0.0
        self._warnings.clear()
        self._errors.clear()

    def _add_warning(self, message: str) -> None:
        """
        Add a warning message.

        Args:
            message: Warning message to add
        """
        self._warnings.append(message)

    def _add_error(self, message: str) -> None:
        """
        Add an error message.

        Args:
            message: Error message to add
        """
        self._errors.append(message)

    def get_config_parameter(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration parameter.

        Args:
            key: Parameter key
            default: Default value if key not found

        Returns:
            Parameter value or default
        """
        return self.config.get(key, default)

    def set_config_parameter(self, key: str, value: Any) -> None:
        """
        Set a configuration parameter.

        Args:
            key: Parameter key
            value: Parameter value
        """
        self.config[key] = value

    def __repr__(self) -> str:
        """Return string representation of the processor."""
        return f"{self.__class__.__name__}(config={self.config})" 