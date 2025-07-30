"""
Tests for the core module of microflex.

This module contains unit tests for core functionality including
types, exceptions, and base classes.
"""

import pytest
import numpy as np
from datetime import datetime

from microflex.core.types import (
    SequenceData,
    QualityData,
    TaxonomyResult,
    DiversityMetrics,
    ProcessingResult,
    SequencingTechnology,
)
from microflex.core.exceptions import (
    MicroflexError,
    ValidationError,
    ProcessingError,
    ClassificationError,
)
from microflex.core.base import BaseProcessor
from microflex.core.config import Config, ProcessingConfig


class TestSequenceData:
    """Test cases for SequenceData class."""

    def test_sequence_data_creation(self):
        """Test basic SequenceData creation."""
        seq_data = SequenceData(
            sequence="ATCGATCG",
            sequence_id="seq1",
            description="Test sequence"
        )
        
        assert seq_data.sequence == "ATCGATCG"
        assert seq_data.sequence_id == "seq1"
        assert seq_data.description == "Test sequence"
        assert seq_data.length == 8
        assert seq_data.technology == SequencingTechnology.UNKNOWN

    def test_sequence_data_with_quality(self):
        """Test SequenceData with quality information."""
        quality_scores = np.array([30, 35, 40, 25, 30, 35, 40, 25])
        quality_data = QualityData(
            scores=quality_scores,
            mean_quality=31.25,
            min_quality=25.0,
            max_quality=40.0,
            length=8
        )
        
        seq_data = SequenceData(
            sequence="ATCGATCG",
            sequence_id="seq1",
            quality=quality_data
        )
        
        assert seq_data.quality is not None
        assert seq_data.quality.mean_quality == 31.25
        assert len(seq_data.quality.scores) == 8

    def test_sequence_data_validation(self):
        """Test SequenceData validation."""
        # Empty sequence should raise error
        with pytest.raises(ValueError):
            SequenceData(sequence="", sequence_id="seq1")
        
        # Empty sequence ID should raise error
        with pytest.raises(ValueError):
            SequenceData(sequence="ATCG", sequence_id="")

    def test_to_seqrecord(self):
        """Test conversion to BioPython SeqRecord."""
        seq_data = SequenceData(
            sequence="ATCGATCG",
            sequence_id="seq1",
            description="Test sequence"
        )
        
        record = seq_data.to_seqrecord()
        assert str(record.seq) == "ATCGATCG"
        assert record.id == "seq1"
        assert record.description == "Test sequence"


class TestQualityData:
    """Test cases for QualityData class."""

    def test_quality_data_creation(self):
        """Test basic QualityData creation."""
        scores = np.array([30, 35, 40, 25])
        quality_data = QualityData(
            scores=scores,
            mean_quality=32.5,
            min_quality=25.0,
            max_quality=40.0,
            length=4
        )
        
        assert len(quality_data.scores) == 4
        assert quality_data.mean_quality == 32.5
        assert quality_data.length == 4

    def test_quality_data_validation(self):
        """Test QualityData validation."""
        scores = np.array([30, 35, 40])
        
        # Length mismatch should raise error
        with pytest.raises(ValueError):
            QualityData(
                scores=scores,
                mean_quality=35.0,
                min_quality=30.0,
                max_quality=40.0,
                length=5  # Wrong length
            )


class TestTaxonomyResult:
    """Test cases for TaxonomyResult class."""

    def test_taxonomy_result_creation(self):
        """Test basic TaxonomyResult creation."""
        taxonomy = TaxonomyResult(
            sequence_id="seq1",
            kingdom="Bacteria",
            phylum="Proteobacteria",
            class_="Gammaproteobacteria",
            order="Enterobacterales",
            family="Enterobacteriaceae",
            genus="Escherichia",
            species="coli",
            confidence=0.95
        )
        
        assert taxonomy.sequence_id == "seq1"
        assert taxonomy.kingdom == "Bacteria"
        assert taxonomy.species == "coli"
        assert taxonomy.confidence == 0.95

    def test_full_taxonomy(self):
        """Test full taxonomy string generation."""
        taxonomy = TaxonomyResult(
            sequence_id="seq1",
            kingdom="Bacteria",
            phylum="Proteobacteria",
            genus="Escherichia",
            species="coli"
        )
        
        expected = "Bacteria;Proteobacteria;Unknown;Unknown;Unknown;Escherichia;coli"
        assert taxonomy.full_taxonomy == expected

    def test_lowest_classification(self):
        """Test lowest classification detection."""
        # Complete taxonomy
        taxonomy1 = TaxonomyResult(
            sequence_id="seq1",
            kingdom="Bacteria",
            genus="Escherichia",
            species="coli"
        )
        assert taxonomy1.lowest_classification == "coli"
        
        # Only genus level
        taxonomy2 = TaxonomyResult(
            sequence_id="seq2",
            kingdom="Bacteria",
            genus="Escherichia"
        )
        assert taxonomy2.lowest_classification == "Escherichia"
        
        # No classification
        taxonomy3 = TaxonomyResult(sequence_id="seq3")
        assert taxonomy3.lowest_classification == "Unclassified"


class TestExceptions:
    """Test cases for custom exceptions."""

    def test_microflex_error(self):
        """Test base MicroflexError."""
        error = MicroflexError("Test error", {"key": "value"})
        assert str(error) == "Test error. Details: {'key': 'value'}"
        assert error.message == "Test error"
        assert error.details == {"key": "value"}

    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("Validation failed")
        assert isinstance(error, MicroflexError)
        assert str(error) == "Validation failed"

    def test_processing_error(self):
        """Test ProcessingError."""
        error = ProcessingError("Processing failed")
        assert isinstance(error, MicroflexError)
        assert str(error) == "Processing failed"


class TestBaseProcessor:
    """Test cases for BaseProcessor class."""

    def test_base_processor_creation(self):
        """Test BaseProcessor creation."""
        processor = BaseProcessor(param1="value1", param2=42)
        assert processor.config == {"param1": "value1", "param2": 42}

    def test_config_methods(self):
        """Test configuration methods."""
        processor = BaseProcessor(param1="value1")
        
        # Test get_config_parameter
        assert processor.get_config_parameter("param1") == "value1"
        assert processor.get_config_parameter("missing", "default") == "default"
        
        # Test set_config_parameter
        processor.set_config_parameter("param2", "value2")
        assert processor.config["param2"] == "value2"

    def test_validation(self):
        """Test input validation."""
        processor = BaseProcessor()
        
        # Valid input
        valid_data = [
            SequenceData(sequence="ATCG", sequence_id="seq1"),
            SequenceData(sequence="GCTA", sequence_id="seq2")
        ]
        assert processor.validate_input(valid_data) is True
        
        # Empty input
        assert processor.validate_input([]) is False
        
        # Invalid input type
        assert processor.validate_input("not a list") is False


class TestConfig:
    """Test cases for Config class."""

    def test_config_creation(self):
        """Test Config creation with defaults."""
        config = Config()
        
        assert isinstance(config.processing, ProcessingConfig)
        assert config.processing.min_length == 100
        assert config.processing.min_quality == 20.0
        assert config.classification.database == "16S_ribosomal_RNA"

    def test_config_to_dict(self):
        """Test configuration serialization."""
        config = Config()
        config_dict = config.to_dict()
        
        assert "processing" in config_dict
        assert "classification" in config_dict
        assert "analysis" in config_dict
        assert "visualization" in config_dict
        
        assert config_dict["processing"]["min_length"] == 100

    def test_config_update(self):
        """Test configuration updates."""
        config = Config()
        
        config.update(
            processing={"min_length": 200, "min_quality": 25.0}
        )
        
        assert config.processing.min_length == 200
        assert config.processing.min_quality == 25.0


if __name__ == "__main__":
    pytest.main([__file__]) 