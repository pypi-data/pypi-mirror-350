"""
FASTQ file reader for the microflex library.

This module provides functionality to read FASTQ files and convert them
to the internal SequenceData format.
"""

import gzip
from pathlib import Path
from typing import Iterator, Optional

import numpy as np
from Bio import SeqIO

from microflex.core.exceptions import IOError, ValidationError
from microflex.core.types import (
    SequenceData,
    SequenceCollection,
    QualityData,
    SequencingTechnology,
    FilePath,
)


class FastqReader:
    """
    Reader for FASTQ format files.

    This class handles reading FASTQ files (both compressed and uncompressed)
    and converts them to the internal SequenceData format with quality scores.
    """

    def __init__(self, technology: SequencingTechnology = SequencingTechnology.UNKNOWN) -> None:
        """
        Initialize FASTQ reader.

        Args:
            technology: Sequencing technology used to generate the data
        """
        self.technology = technology

    def read(self, file_path: FilePath) -> SequenceCollection:
        """
        Read sequences from FASTQ file.

        Args:
            file_path: Path to the FASTQ file

        Returns:
            Collection of sequence data

        Raises:
            IOError: If file cannot be read
            ValidationError: If file format is invalid
        """
        path = Path(file_path)
        
        if not path.exists():
            raise IOError(f"File not found: {file_path}")

        if not self.validate_format(file_path):
            raise ValidationError(f"Invalid FASTQ format: {file_path}")

        sequences = []
        
        try:
            for record in self._parse_fastq(path):
                sequences.append(record)
                
        except Exception as e:
            raise IOError(f"Failed to read FASTQ file {file_path}: {e}") from e

        return sequences

    def read_iterator(self, file_path: FilePath) -> Iterator[SequenceData]:
        """
        Read sequences from FASTQ file as iterator.

        Args:
            file_path: Path to the FASTQ file

        Yields:
            Individual sequence data objects

        Raises:
            IOError: If file cannot be read
            ValidationError: If file format is invalid
        """
        path = Path(file_path)
        
        if not path.exists():
            raise IOError(f"File not found: {file_path}")

        if not self.validate_format(file_path):
            raise ValidationError(f"Invalid FASTQ format: {file_path}")

        try:
            yield from self._parse_fastq(path)
        except Exception as e:
            raise IOError(f"Failed to read FASTQ file {file_path}: {e}") from e

    def _parse_fastq(self, path: Path) -> Iterator[SequenceData]:
        """
        Parse FASTQ file and yield SequenceData objects.

        Args:
            path: Path to the FASTQ file

        Yields:
            SequenceData objects
        """
        # Determine if file is compressed
        is_compressed = path.suffix.lower() == '.gz'
        
        if is_compressed:
            file_handle = gzip.open(path, 'rt', encoding='utf-8')
        else:
            file_handle = open(path, 'r', encoding='utf-8')

        try:
            for record in SeqIO.parse(file_handle, 'fastq'):
                # Extract quality scores
                quality_scores = np.array(record.letter_annotations.get('phred_quality', []))
                
                # Create quality data if available
                quality_data = None
                if len(quality_scores) > 0:
                    quality_data = QualityData(
                        scores=quality_scores,
                        mean_quality=float(np.mean(quality_scores)),
                        min_quality=float(np.min(quality_scores)),
                        max_quality=float(np.max(quality_scores)),
                        length=len(quality_scores)
                    )

                # Create sequence data
                seq_data = SequenceData(
                    sequence=str(record.seq),
                    sequence_id=record.id,
                    description=record.description,
                    quality=quality_data,
                    technology=self.technology,
                    metadata={
                        'source_file': str(path),
                        'format': 'fastq',
                    }
                )

                yield seq_data

        finally:
            file_handle.close()

    def validate_format(self, file_path: FilePath) -> bool:
        """
        Validate if file is in FASTQ format.

        Args:
            file_path: Path to the file

        Returns:
            True if file is valid FASTQ, False otherwise
        """
        path = Path(file_path)
        
        if not path.exists():
            return False

        try:
            # Try to read first few records
            is_compressed = path.suffix.lower() == '.gz'
            
            if is_compressed:
                file_handle = gzip.open(path, 'rt', encoding='utf-8')
            else:
                file_handle = open(path, 'r', encoding='utf-8')

            try:
                # Read first 4 lines to check FASTQ format
                lines = []
                for i, line in enumerate(file_handle):
                    lines.append(line.strip())
                    if i >= 3:  # Read first record (4 lines)
                        break

                if len(lines) < 4:
                    return False

                # Check FASTQ format structure
                # Line 1: starts with @
                # Line 2: sequence
                # Line 3: starts with +
                # Line 4: quality scores (same length as sequence)
                if (not lines[0].startswith('@') or
                    not lines[2].startswith('+') or
                    len(lines[1]) != len(lines[3])):
                    return False

                # Try to parse with BioPython to be sure
                file_handle.seek(0)
                next(SeqIO.parse(file_handle, 'fastq'))
                return True

            finally:
                file_handle.close()

        except Exception:
            return False

    def count_sequences(self, file_path: FilePath) -> int:
        """
        Count number of sequences in FASTQ file.

        Args:
            file_path: Path to the FASTQ file

        Returns:
            Number of sequences

        Raises:
            IOError: If file cannot be read
        """
        path = Path(file_path)
        
        if not path.exists():
            raise IOError(f"File not found: {file_path}")

        try:
            count = 0
            is_compressed = path.suffix.lower() == '.gz'
            
            if is_compressed:
                file_handle = gzip.open(path, 'rt', encoding='utf-8')
            else:
                file_handle = open(path, 'r', encoding='utf-8')

            try:
                for _ in SeqIO.parse(file_handle, 'fastq'):
                    count += 1
            finally:
                file_handle.close()

            return count

        except Exception as e:
            raise IOError(f"Failed to count sequences in {file_path}: {e}") from e

    def get_sequence_lengths(self, file_path: FilePath) -> list[int]:
        """
        Get lengths of all sequences in FASTQ file.

        Args:
            file_path: Path to the FASTQ file

        Returns:
            List of sequence lengths

        Raises:
            IOError: If file cannot be read
        """
        lengths = []
        
        try:
            for seq_data in self.read_iterator(file_path):
                lengths.append(seq_data.length)
        except Exception as e:
            raise IOError(f"Failed to get sequence lengths from {file_path}: {e}") from e

        return lengths

    def get_quality_stats(self, file_path: FilePath) -> dict[str, float]:
        """
        Get quality statistics for all sequences in FASTQ file.

        Args:
            file_path: Path to the FASTQ file

        Returns:
            Dictionary with quality statistics

        Raises:
            IOError: If file cannot be read
        """
        all_qualities = []
        
        try:
            for seq_data in self.read_iterator(file_path):
                if seq_data.quality:
                    all_qualities.extend(seq_data.quality.scores)
        except Exception as e:
            raise IOError(f"Failed to get quality stats from {file_path}: {e}") from e

        if not all_qualities:
            return {}

        qualities = np.array(all_qualities)
        
        return {
            'mean_quality': float(np.mean(qualities)),
            'median_quality': float(np.median(qualities)),
            'min_quality': float(np.min(qualities)),
            'max_quality': float(np.max(qualities)),
            'std_quality': float(np.std(qualities)),
            'q25': float(np.percentile(qualities, 25)),
            'q75': float(np.percentile(qualities, 75)),
        } 