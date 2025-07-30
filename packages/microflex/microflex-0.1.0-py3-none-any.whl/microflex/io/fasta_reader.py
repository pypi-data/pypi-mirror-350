"""
FASTA file reader for the microflex library.

This module provides functionality to read FASTA files and convert them
to the internal SequenceData format.
"""

import gzip
from pathlib import Path
from typing import Iterator, Optional

from Bio import SeqIO

from microflex.core.exceptions import IOError, ValidationError
from microflex.core.types import (
    SequenceData,
    SequenceCollection,
    SequencingTechnology,
    FilePath,
)


class FastaReader:
    """
    Reader for FASTA format files.

    This class handles reading FASTA files (both compressed and uncompressed)
    and converts them to the internal SequenceData format.
    """

    def __init__(self, technology: SequencingTechnology = SequencingTechnology.UNKNOWN) -> None:
        """
        Initialize FASTA reader.

        Args:
            technology: Sequencing technology used to generate the data
        """
        self.technology = technology

    def read(self, file_path: FilePath) -> SequenceCollection:
        """
        Read sequences from FASTA file.

        Args:
            file_path: Path to the FASTA file

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
            raise ValidationError(f"Invalid FASTA format: {file_path}")

        sequences = []
        
        try:
            for record in self._parse_fasta(path):
                sequences.append(record)
                
        except Exception as e:
            raise IOError(f"Failed to read FASTA file {file_path}: {e}") from e

        return sequences

    def read_iterator(self, file_path: FilePath) -> Iterator[SequenceData]:
        """
        Read sequences from FASTA file as iterator.

        Args:
            file_path: Path to the FASTA file

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
            raise ValidationError(f"Invalid FASTA format: {file_path}")

        try:
            yield from self._parse_fasta(path)
        except Exception as e:
            raise IOError(f"Failed to read FASTA file {file_path}: {e}") from e

    def _parse_fasta(self, path: Path) -> Iterator[SequenceData]:
        """
        Parse FASTA file and yield SequenceData objects.

        Args:
            path: Path to the FASTA file

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
            for record in SeqIO.parse(file_handle, 'fasta'):
                # Create sequence data
                seq_data = SequenceData(
                    sequence=str(record.seq),
                    sequence_id=record.id,
                    description=record.description,
                    quality=None,  # FASTA files don't have quality scores
                    technology=self.technology,
                    metadata={
                        'source_file': str(path),
                        'format': 'fasta',
                    }
                )

                yield seq_data

        finally:
            file_handle.close()

    def validate_format(self, file_path: FilePath) -> bool:
        """
        Validate if file is in FASTA format.

        Args:
            file_path: Path to the file

        Returns:
            True if file is valid FASTA, False otherwise
        """
        path = Path(file_path)
        
        if not path.exists():
            return False

        try:
            # Try to read first few lines
            is_compressed = path.suffix.lower() == '.gz'
            
            if is_compressed:
                file_handle = gzip.open(path, 'rt', encoding='utf-8')
            else:
                file_handle = open(path, 'r', encoding='utf-8')

            try:
                # Read first few lines to check FASTA format
                lines = []
                for i, line in enumerate(file_handle):
                    lines.append(line.strip())
                    if i >= 10:  # Read first few lines
                        break

                if not lines:
                    return False

                # Check FASTA format structure
                # First line should start with >
                if not lines[0].startswith('>'):
                    return False

                # Should have sequence lines after header
                has_sequence = any(line and not line.startswith('>') for line in lines[1:])
                if not has_sequence:
                    return False

                # Try to parse with BioPython to be sure
                file_handle.seek(0)
                next(SeqIO.parse(file_handle, 'fasta'))
                return True

            finally:
                file_handle.close()

        except Exception:
            return False

    def count_sequences(self, file_path: FilePath) -> int:
        """
        Count number of sequences in FASTA file.

        Args:
            file_path: Path to the FASTA file

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
                for _ in SeqIO.parse(file_handle, 'fasta'):
                    count += 1
            finally:
                file_handle.close()

            return count

        except Exception as e:
            raise IOError(f"Failed to count sequences in {file_path}: {e}") from e

    def get_sequence_lengths(self, file_path: FilePath) -> list[int]:
        """
        Get lengths of all sequences in FASTA file.

        Args:
            file_path: Path to the FASTA file

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

    def get_sequence_stats(self, file_path: FilePath) -> dict[str, float]:
        """
        Get sequence statistics for all sequences in FASTA file.

        Args:
            file_path: Path to the FASTA file

        Returns:
            Dictionary with sequence statistics

        Raises:
            IOError: If file cannot be read
        """
        lengths = self.get_sequence_lengths(file_path)
        
        if not lengths:
            return {}

        import numpy as np
        lengths_array = np.array(lengths)
        
        return {
            'total_sequences': len(lengths),
            'mean_length': float(np.mean(lengths_array)),
            'median_length': float(np.median(lengths_array)),
            'min_length': float(np.min(lengths_array)),
            'max_length': float(np.max(lengths_array)),
            'std_length': float(np.std(lengths_array)),
            'total_bases': int(np.sum(lengths_array)),
        } 