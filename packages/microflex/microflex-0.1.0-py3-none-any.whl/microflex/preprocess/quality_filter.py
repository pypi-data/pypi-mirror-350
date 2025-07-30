"""
Quality filtering for the microflex library.

This module provides quality control and filtering functionality
for sequence data based on various criteria.
"""

from typing import Optional, List, Callable

import numpy as np

from microflex.core.base import BaseProcessor
from microflex.core.exceptions import ValidationError, ProcessingError
from microflex.core.types import SequenceData, SequenceCollection


class QualityFilter(BaseProcessor):
    """
    Quality filter for sequence data.

    This processor filters sequences based on quality scores, length,
    and other quality criteria.
    """

    def __init__(
        self,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        min_quality: Optional[float] = None,
        min_mean_quality: Optional[float] = None,
        max_n_content: Optional[float] = None,
        trim_ends: bool = False,
        trim_quality_threshold: float = 20.0,
        **kwargs
    ) -> None:
        """
        Initialize quality filter.

        Args:
            min_length: Minimum sequence length
            max_length: Maximum sequence length
            min_quality: Minimum quality score for any base
            min_mean_quality: Minimum mean quality score
            max_n_content: Maximum fraction of N bases (0.0-1.0)
            trim_ends: Whether to trim low-quality ends
            trim_quality_threshold: Quality threshold for trimming
            **kwargs: Additional configuration parameters
        """
        super().__init__(
            min_length=min_length,
            max_length=max_length,
            min_quality=min_quality,
            min_mean_quality=min_mean_quality,
            max_n_content=max_n_content,
            trim_ends=trim_ends,
            trim_quality_threshold=trim_quality_threshold,
            **kwargs
        )

        # Validate parameters
        if min_length is not None and min_length < 1:
            raise ValidationError("min_length must be >= 1")
        
        if max_length is not None and max_length < 1:
            raise ValidationError("max_length must be >= 1")
            
        if min_length is not None and max_length is not None and min_length > max_length:
            raise ValidationError("min_length must be <= max_length")
            
        if min_quality is not None and (min_quality < 0 or min_quality > 50):
            raise ValidationError("min_quality must be between 0 and 50")
            
        if min_mean_quality is not None and (min_mean_quality < 0 or min_mean_quality > 50):
            raise ValidationError("min_mean_quality must be between 0 and 50")
            
        if max_n_content is not None and (max_n_content < 0 or max_n_content > 1):
            raise ValidationError("max_n_content must be between 0.0 and 1.0")

    def _process_implementation(self, data: SequenceCollection) -> SequenceCollection:
        """
        Apply quality filtering to sequences.

        Args:
            data: Input sequence collection

        Returns:
            Filtered sequence collection
        """
        filtered_sequences = []
        
        for seq_data in data:
            try:
                # Apply trimming if requested
                if self.get_config_parameter('trim_ends', False):
                    seq_data = self._trim_sequence(seq_data)
                
                # Apply filters
                if self._passes_filters(seq_data):
                    filtered_sequences.append(seq_data)
                else:
                    self._add_warning(f"Sequence {seq_data.sequence_id} filtered out")
                    
            except Exception as e:
                self._add_error(f"Error processing sequence {seq_data.sequence_id}: {e}")
                continue

        return filtered_sequences

    def _passes_filters(self, seq_data: SequenceData) -> bool:
        """
        Check if sequence passes all filters.

        Args:
            seq_data: Sequence data to check

        Returns:
            True if sequence passes all filters
        """
        # Length filters
        min_length = self.get_config_parameter('min_length')
        max_length = self.get_config_parameter('max_length')
        
        if min_length is not None and seq_data.length < min_length:
            return False
            
        if max_length is not None and seq_data.length > max_length:
            return False

        # Quality filters (only if quality data is available)
        if seq_data.quality is not None:
            min_quality = self.get_config_parameter('min_quality')
            min_mean_quality = self.get_config_parameter('min_mean_quality')
            
            if min_quality is not None and seq_data.quality.min_quality < min_quality:
                return False
                
            if min_mean_quality is not None and seq_data.quality.mean_quality < min_mean_quality:
                return False

        # N content filter
        max_n_content = self.get_config_parameter('max_n_content')
        if max_n_content is not None:
            n_count = seq_data.sequence.upper().count('N')
            n_fraction = n_count / seq_data.length if seq_data.length > 0 else 0
            if n_fraction > max_n_content:
                return False

        return True

    def _trim_sequence(self, seq_data: SequenceData) -> SequenceData:
        """
        Trim low-quality ends from sequence.

        Args:
            seq_data: Sequence data to trim

        Returns:
            Trimmed sequence data
        """
        if seq_data.quality is None:
            # Cannot trim without quality data
            return seq_data

        threshold = self.get_config_parameter('trim_quality_threshold', 20.0)
        quality_scores = seq_data.quality.scores
        
        # Find trim positions
        start_pos = 0
        end_pos = len(quality_scores)
        
        # Trim from start
        for i, score in enumerate(quality_scores):
            if score >= threshold:
                start_pos = i
                break
        else:
            # All bases are low quality
            start_pos = len(quality_scores)
        
        # Trim from end
        for i in range(len(quality_scores) - 1, -1, -1):
            if quality_scores[i] >= threshold:
                end_pos = i + 1
                break
        else:
            # All bases are low quality
            end_pos = 0

        # Check if anything remains
        if start_pos >= end_pos:
            # Sequence completely trimmed
            return SequenceData(
                sequence="",
                sequence_id=seq_data.sequence_id,
                description=seq_data.description,
                quality=None,
                technology=seq_data.technology,
                metadata={**seq_data.metadata, 'trimmed': 'completely'}
            )

        # Create trimmed sequence
        trimmed_sequence = seq_data.sequence[start_pos:end_pos]
        trimmed_scores = quality_scores[start_pos:end_pos]
        
        # Create new quality data
        from microflex.core.types import QualityData
        trimmed_quality = QualityData(
            scores=trimmed_scores,
            mean_quality=float(np.mean(trimmed_scores)),
            min_quality=float(np.min(trimmed_scores)),
            max_quality=float(np.max(trimmed_scores)),
            length=len(trimmed_scores)
        )

        # Create trimmed sequence data
        return SequenceData(
            sequence=trimmed_sequence,
            sequence_id=seq_data.sequence_id,
            description=seq_data.description,
            quality=trimmed_quality,
            technology=seq_data.technology,
            metadata={
                **seq_data.metadata,
                'trimmed': True,
                'trim_start': start_pos,
                'trim_end': end_pos,
                'original_length': seq_data.length
            }
        )

    def get_filter_stats(self, original_data: SequenceCollection, filtered_data: SequenceCollection) -> dict:
        """
        Get filtering statistics.

        Args:
            original_data: Original sequence collection
            filtered_data: Filtered sequence collection

        Returns:
            Dictionary with filtering statistics
        """
        stats = {
            'total_input': len(original_data),
            'total_output': len(filtered_data),
            'filtered_count': len(original_data) - len(filtered_data),
            'pass_rate': len(filtered_data) / len(original_data) if original_data else 0,
        }

        # Length statistics
        if original_data:
            original_lengths = [seq.length for seq in original_data]
            stats['original_mean_length'] = np.mean(original_lengths)
            stats['original_median_length'] = np.median(original_lengths)

        if filtered_data:
            filtered_lengths = [seq.length for seq in filtered_data]
            stats['filtered_mean_length'] = np.mean(filtered_lengths)
            stats['filtered_median_length'] = np.median(filtered_lengths)

        # Quality statistics (if available)
        original_qualities = [seq.quality.mean_quality for seq in original_data if seq.quality]
        filtered_qualities = [seq.quality.mean_quality for seq in filtered_data if seq.quality]

        if original_qualities:
            stats['original_mean_quality'] = np.mean(original_qualities)
            stats['original_median_quality'] = np.median(original_qualities)

        if filtered_qualities:
            stats['filtered_mean_quality'] = np.mean(filtered_qualities)
            stats['filtered_median_quality'] = np.median(filtered_qualities)

        return stats


class LengthFilter(QualityFilter):
    """
    Simple length-based filter.

    This is a specialized version of QualityFilter that only filters
    based on sequence length.
    """

    def __init__(self, min_length: int, max_length: Optional[int] = None, **kwargs) -> None:
        """
        Initialize length filter.

        Args:
            min_length: Minimum sequence length
            max_length: Maximum sequence length
            **kwargs: Additional configuration parameters
        """
        super().__init__(
            min_length=min_length,
            max_length=max_length,
            min_quality=None,
            min_mean_quality=None,
            max_n_content=None,
            trim_ends=False,
            **kwargs
        )


class QualityScoreFilter(QualityFilter):
    """
    Quality score-based filter.

    This is a specialized version of QualityFilter that only filters
    based on quality scores.
    """

    def __init__(
        self,
        min_mean_quality: float,
        min_quality: Optional[float] = None,
        **kwargs
    ) -> None:
        """
        Initialize quality score filter.

        Args:
            min_mean_quality: Minimum mean quality score
            min_quality: Minimum quality score for any base
            **kwargs: Additional configuration parameters
        """
        super().__init__(
            min_length=None,
            max_length=None,
            min_quality=min_quality,
            min_mean_quality=min_mean_quality,
            max_n_content=None,
            trim_ends=False,
            **kwargs
        ) 