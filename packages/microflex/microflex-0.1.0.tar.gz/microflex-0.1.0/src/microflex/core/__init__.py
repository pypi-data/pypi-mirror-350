"""
Core module for microflex.

This module contains the fundamental abstractions, interfaces, and base classes
that are used throughout the microflex library.
"""

from microflex.core.base import BaseProcessor
from microflex.core.config import Config
from microflex.core.exceptions import (
    MicroflexError,
    ValidationError,
    ProcessingError,
    ClassificationError,
    IOError as MicroflexIOError,
)
from microflex.core.interfaces import (
    DataReader,
    DataWriter,
    Processor,
    Classifier,
    Analyzer,
    Visualizer,
)
from microflex.core.types import (
    SequenceData,
    QualityData,
    TaxonomyResult,
    DiversityMetrics,
    ProcessingResult,
)

__all__ = [
    "BaseProcessor",
    "Config",
    "MicroflexError",
    "ValidationError",
    "ProcessingError",
    "ClassificationError",
    "MicroflexIOError",
    "DataReader",
    "DataWriter",
    "Processor",
    "Classifier",
    "Analyzer",
    "Visualizer",
    "SequenceData",
    "QualityData",
    "TaxonomyResult",
    "DiversityMetrics",
    "ProcessingResult",
] 