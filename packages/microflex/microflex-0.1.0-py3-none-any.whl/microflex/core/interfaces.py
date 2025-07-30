"""
Abstract interfaces and protocols for the microflex library.

This module defines the core interfaces that all components must implement
to ensure consistency and interoperability throughout the library.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Union

from microflex.core.types import (
    SequenceData,
    SequenceCollection,
    TaxonomyResult,
    TaxonomyCollection,
    DiversityMetrics,
    ProcessingResult,
    FilePath,
)


class DataReader(Protocol):
    """Protocol for data reading operations."""

    def read(self, file_path: FilePath) -> SequenceCollection:
        """
        Read sequence data from file.

        Args:
            file_path: Path to the input file

        Returns:
            Collection of sequence data
        """
        ...

    def validate_format(self, file_path: FilePath) -> bool:
        """
        Validate if file format is supported.

        Args:
            file_path: Path to the file to validate

        Returns:
            True if format is supported, False otherwise
        """
        ...


class DataWriter(Protocol):
    """Protocol for data writing operations."""

    def write(
        self,
        data: Union[SequenceCollection, TaxonomyCollection],
        file_path: FilePath,
        **kwargs: Any,
    ) -> None:
        """
        Write data to file.

        Args:
            data: Data to write
            file_path: Path to the output file
            **kwargs: Additional writing parameters
        """
        ...


class Processor(ABC):
    """Abstract base class for data processors."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize processor with configuration parameters."""
        self.config = kwargs

    @abstractmethod
    def process(self, data: SequenceCollection) -> SequenceCollection:
        """
        Process sequence data.

        Args:
            data: Input sequence collection

        Returns:
            Processed sequence collection
        """
        pass

    @abstractmethod
    def validate_input(self, data: SequenceCollection) -> bool:
        """
        Validate input data.

        Args:
            data: Input data to validate

        Returns:
            True if data is valid, False otherwise
        """
        pass

    def get_processing_stats(self) -> ProcessingResult:
        """
        Get processing statistics.

        Returns:
            Processing result with statistics
        """
        # Default implementation - subclasses should override
        return ProcessingResult(
            input_count=0,
            output_count=0,
            filtered_count=0,
            processing_time=0.0,
            parameters=self.config,
        )


class Classifier(ABC):
    """Abstract base class for taxonomic classifiers."""

    def __init__(self, database: Optional[str] = None, **kwargs: Any) -> None:
        """
        Initialize classifier.

        Args:
            database: Path or name of the reference database
            **kwargs: Additional configuration parameters
        """
        self.database = database
        self.config = kwargs

    @abstractmethod
    def classify(self, sequences: SequenceCollection) -> TaxonomyCollection:
        """
        Classify sequences taxonomically.

        Args:
            sequences: Input sequence collection

        Returns:
            Taxonomy classification results
        """
        pass

    @abstractmethod
    def validate_database(self) -> bool:
        """
        Validate that the reference database is available and valid.

        Returns:
            True if database is valid, False otherwise
        """
        pass

    def get_supported_databases(self) -> List[str]:
        """
        Get list of supported databases.

        Returns:
            List of supported database names
        """
        return []


class Analyzer(ABC):
    """Abstract base class for analysis operations."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize analyzer with configuration parameters."""
        self.config = kwargs

    @abstractmethod
    def analyze(self, data: TaxonomyCollection) -> Dict[str, Any]:
        """
        Perform analysis on taxonomic data.

        Args:
            data: Input taxonomy collection

        Returns:
            Analysis results
        """
        pass

    def validate_input(self, data: TaxonomyCollection) -> bool:
        """
        Validate input data for analysis.

        Args:
            data: Input data to validate

        Returns:
            True if data is valid, False otherwise
        """
        return len(data) > 0


class Visualizer(ABC):
    """Abstract base class for visualization operations."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize visualizer with configuration parameters."""
        self.config = kwargs

    @abstractmethod
    def plot(self, data: Any, output_path: Optional[FilePath] = None) -> Any:
        """
        Create visualization from data.

        Args:
            data: Input data to visualize
            output_path: Optional path to save the plot

        Returns:
            Plot object or figure
        """
        pass

    def save_plot(self, plot: Any, output_path: FilePath, **kwargs: Any) -> None:
        """
        Save plot to file.

        Args:
            plot: Plot object to save
            output_path: Path to save the plot
            **kwargs: Additional saving parameters
        """
        pass


class Pipeline(ABC):
    """Abstract base class for analysis pipelines."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize pipeline with configuration parameters."""
        self.config = kwargs
        self.processors: List[Processor] = []
        self.results: Dict[str, Any] = {}

    @abstractmethod
    def run(self, input_data: SequenceCollection) -> Dict[str, Any]:
        """
        Run the complete pipeline.

        Args:
            input_data: Input sequence collection

        Returns:
            Pipeline results
        """
        pass

    def add_processor(self, processor: Processor) -> None:
        """
        Add a processor to the pipeline.

        Args:
            processor: Processor to add
        """
        self.processors.append(processor)

    def get_results(self) -> Dict[str, Any]:
        """
        Get pipeline results.

        Returns:
            Dictionary containing all pipeline results
        """
        return self.results


class ConfigurableComponent(Protocol):
    """Protocol for components that can be configured."""

    def configure(self, config: Dict[str, Any]) -> None:
        """
        Configure the component.

        Args:
            config: Configuration dictionary
        """
        ...

    def get_config(self) -> Dict[str, Any]:
        """
        Get current configuration.

        Returns:
            Current configuration dictionary
        """
        ...


class Cacheable(Protocol):
    """Protocol for components that support caching."""

    def enable_cache(self, cache_dir: FilePath) -> None:
        """
        Enable caching for the component.

        Args:
            cache_dir: Directory to store cache files
        """
        ...

    def clear_cache(self) -> None:
        """Clear all cached data."""
        ...

    def is_cached(self, key: str) -> bool:
        """
        Check if result is cached.

        Args:
            key: Cache key to check

        Returns:
            True if result is cached, False otherwise
        """
        ... 