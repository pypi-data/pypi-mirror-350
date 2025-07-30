"""
Type definitions and data structures for the microflex library.

This module defines all the core data types, protocols, and type aliases
used throughout the microflex library.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Union
from datetime import datetime

import numpy as np
import pandas as pd
from Bio.SeqRecord import SeqRecord


class SequencingTechnology(Enum):
    """Enumeration of supported sequencing technologies."""

    ILLUMINA = "illumina"
    NANOPORE = "nanopore"
    SANGER = "sanger"
    UNKNOWN = "unknown"


class FileFormat(Enum):
    """Enumeration of supported file formats."""

    FASTQ = "fastq"
    FASTA = "fasta"
    AB1 = "ab1"
    QZA = "qza"
    BIOM = "biom"
    TSV = "tsv"
    CSV = "csv"


@dataclass
class QualityData:
    """Container for sequence quality information."""

    scores: np.ndarray
    mean_quality: float
    min_quality: float
    max_quality: float
    length: int

    def __post_init__(self) -> None:
        """Validate quality data after initialization."""
        if len(self.scores) != self.length:
            raise ValueError("Quality scores length must match sequence length")


@dataclass
class SequenceData:
    """Container for sequence data with metadata."""

    sequence: str
    sequence_id: str
    description: Optional[str] = None
    quality: Optional[QualityData] = None
    technology: SequencingTechnology = SequencingTechnology.UNKNOWN
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate sequence data after initialization."""
        if not self.sequence:
            raise ValueError("Sequence cannot be empty")
        if not self.sequence_id:
            raise ValueError("Sequence ID cannot be empty")

    @property
    def length(self) -> int:
        """Return the length of the sequence."""
        return len(self.sequence)

    def to_seqrecord(self) -> SeqRecord:
        """Convert to BioPython SeqRecord."""
        from Bio.Seq import Seq

        record = SeqRecord(
            Seq(self.sequence),
            id=self.sequence_id,
            description=self.description or "",
        )
        if self.quality:
            record.letter_annotations["phred_quality"] = self.quality.scores
        return record


@dataclass
class TaxonomyResult:
    """Container for taxonomic classification results."""

    sequence_id: str
    kingdom: Optional[str] = None
    phylum: Optional[str] = None
    class_: Optional[str] = None
    order: Optional[str] = None
    family: Optional[str] = None
    genus: Optional[str] = None
    species: Optional[str] = None
    confidence: Optional[float] = None
    method: Optional[str] = None
    database: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def full_taxonomy(self) -> str:
        """Return full taxonomic lineage as string."""
        levels = [
            self.kingdom,
            self.phylum,
            self.class_,
            self.order,
            self.family,
            self.genus,
            self.species,
        ]
        return ";".join(level or "Unknown" for level in levels)

    @property
    def lowest_classification(self) -> str:
        """Return the lowest level of classification."""
        for level in [
            self.species,
            self.genus,
            self.family,
            self.order,
            self.class_,
            self.phylum,
            self.kingdom,
        ]:
            if level:
                return level
        return "Unclassified"


@dataclass
class DiversityMetrics:
    """Container for diversity analysis results."""

    sample_id: str
    observed_otus: int
    shannon: float
    simpson: float
    chao1: Optional[float] = None
    ace: Optional[float] = None
    pielou_evenness: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcessingResult:
    """Container for processing operation results."""

    input_count: int
    output_count: int
    filtered_count: int
    processing_time: float
    parameters: Dict[str, Any]
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculate the success rate of processing."""
        if self.input_count == 0:
            return 0.0
        return self.output_count / self.input_count

    @property
    def filter_rate(self) -> float:
        """Calculate the filter rate of processing."""
        if self.input_count == 0:
            return 0.0
        return self.filtered_count / self.input_count


# Type aliases for common data structures
SequenceCollection = List[SequenceData]
TaxonomyCollection = List[TaxonomyResult]
DiversityCollection = List[DiversityMetrics]
FilePath = Union[str, Path]
DataFrame = pd.DataFrame
Array = np.ndarray


class Serializable(Protocol):
    """Protocol for objects that can be serialized."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert object to dictionary."""
        ...

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Serializable:
        """Create object from dictionary."""
        ... 