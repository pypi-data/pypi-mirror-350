"""
Sequence writer for the microflex library.

This module provides functionality to write sequence data to various formats
including FASTA and FASTQ.
"""

import gzip
from pathlib import Path
from typing import Optional, TextIO, Union

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

from microflex.core.exceptions import IOError, ValidationError
from microflex.core.types import (
    SequenceData,
    SequenceCollection,
    FileFormat,
    FilePath,
)


class SequenceWriter:
    """
    Writer for sequence data in various formats.

    This class handles writing SequenceData objects to files in
    FASTA, FASTQ, and other supported formats.
    """

    def __init__(self) -> None:
        """Initialize sequence writer."""
        pass

    def write(
        self,
        sequences: SequenceCollection,
        file_path: FilePath,
        format: Optional[FileFormat] = None,
        compress: bool = False,
        **kwargs
    ) -> None:
        """
        Write sequences to file.

        Args:
            sequences: Collection of sequence data
            file_path: Path to output file
            format: Output format (auto-detected if None)
            compress: Whether to compress output with gzip
            **kwargs: Additional format-specific parameters

        Raises:
            IOError: If file cannot be written
            ValidationError: If format is not supported
        """
        path = Path(file_path)
        
        if not sequences:
            raise ValidationError("No sequences to write")

        # Auto-detect format if not specified
        if format is None:
            format = self._detect_format_from_path(path)

        # Validate format
        if format not in [FileFormat.FASTA, FileFormat.FASTQ]:
            raise ValidationError(f"Unsupported output format: {format}")

        try:
            # Create output directory if needed
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write sequences
            if compress:
                with gzip.open(path, 'wt', encoding='utf-8') as f:
                    self._write_sequences(f, sequences, format, **kwargs)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    self._write_sequences(f, sequences, format, **kwargs)

        except Exception as e:
            raise IOError(f"Failed to write sequences to {file_path}: {e}") from e

    def _write_sequences(
        self,
        file_handle: TextIO,
        sequences: SequenceCollection,
        format: FileFormat,
        **kwargs
    ) -> None:
        """
        Write sequences to file handle.

        Args:
            file_handle: File handle to write to
            sequences: Collection of sequence data
            format: Output format
            **kwargs: Additional format-specific parameters
        """
        if format == FileFormat.FASTA:
            self._write_fasta(file_handle, sequences, **kwargs)
        elif format == FileFormat.FASTQ:
            self._write_fastq(file_handle, sequences, **kwargs)

    def _write_fasta(
        self,
        file_handle: TextIO,
        sequences: SequenceCollection,
        line_length: int = 80,
        **kwargs
    ) -> None:
        """
        Write sequences in FASTA format.

        Args:
            file_handle: File handle to write to
            sequences: Collection of sequence data
            line_length: Maximum line length for sequences
            **kwargs: Additional parameters
        """
        for seq_data in sequences:
            # Write header
            header = f">{seq_data.sequence_id}"
            if seq_data.description:
                header += f" {seq_data.description}"
            file_handle.write(header + "\n")

            # Write sequence with line wrapping
            sequence = seq_data.sequence
            for i in range(0, len(sequence), line_length):
                file_handle.write(sequence[i:i + line_length] + "\n")

    def _write_fastq(
        self,
        file_handle: TextIO,
        sequences: SequenceCollection,
        **kwargs
    ) -> None:
        """
        Write sequences in FASTQ format.

        Args:
            file_handle: File handle to write to
            sequences: Collection of sequence data
            **kwargs: Additional parameters
        """
        for seq_data in sequences:
            # Check if quality data is available
            if seq_data.quality is None:
                raise ValidationError(
                    f"Sequence {seq_data.sequence_id} has no quality data for FASTQ format"
                )

            # Write FASTQ record
            file_handle.write(f"@{seq_data.sequence_id}")
            if seq_data.description:
                file_handle.write(f" {seq_data.description}")
            file_handle.write("\n")
            
            file_handle.write(seq_data.sequence + "\n")
            file_handle.write("+\n")
            
            # Convert quality scores to ASCII
            quality_string = self._quality_scores_to_string(seq_data.quality.scores)
            file_handle.write(quality_string + "\n")

    def _quality_scores_to_string(self, scores) -> str:
        """
        Convert quality scores to ASCII string.

        Args:
            scores: Array of quality scores

        Returns:
            ASCII quality string
        """
        # Convert Phred scores to ASCII (Phred+33 encoding)
        return ''.join(chr(int(score) + 33) for score in scores)

    def _detect_format_from_path(self, path: Path) -> FileFormat:
        """
        Detect output format from file path.

        Args:
            path: File path

        Returns:
            Detected format

        Raises:
            ValidationError: If format cannot be detected
        """
        # Handle compressed files
        if path.suffix.lower() == '.gz':
            stem_path = Path(path.stem)
            suffix = stem_path.suffix.lower()
        else:
            suffix = path.suffix.lower()

        format_map = {
            '.fasta': FileFormat.FASTA,
            '.fa': FileFormat.FASTA,
            '.fas': FileFormat.FASTA,
            '.fastq': FileFormat.FASTQ,
            '.fq': FileFormat.FASTQ,
        }

        if suffix in format_map:
            return format_map[suffix]

        raise ValidationError(f"Cannot detect format from file extension: {suffix}")

    def write_fasta(
        self,
        sequences: SequenceCollection,
        file_path: FilePath,
        line_length: int = 80,
        compress: bool = False
    ) -> None:
        """
        Write sequences in FASTA format.

        Args:
            sequences: Collection of sequence data
            file_path: Path to output file
            line_length: Maximum line length for sequences
            compress: Whether to compress output with gzip

        Raises:
            IOError: If file cannot be written
        """
        self.write(
            sequences,
            file_path,
            format=FileFormat.FASTA,
            compress=compress,
            line_length=line_length
        )

    def write_fastq(
        self,
        sequences: SequenceCollection,
        file_path: FilePath,
        compress: bool = False
    ) -> None:
        """
        Write sequences in FASTQ format.

        Args:
            sequences: Collection of sequence data
            file_path: Path to output file
            compress: Whether to compress output with gzip

        Raises:
            IOError: If file cannot be written
            ValidationError: If sequences lack quality data
        """
        self.write(
            sequences,
            file_path,
            format=FileFormat.FASTQ,
            compress=compress
        )

    def write_biopython(
        self,
        sequences: SequenceCollection,
        file_path: FilePath,
        format: str,
        compress: bool = False
    ) -> None:
        """
        Write sequences using BioPython SeqIO.

        Args:
            sequences: Collection of sequence data
            file_path: Path to output file
            format: BioPython format string
            compress: Whether to compress output with gzip

        Raises:
            IOError: If file cannot be written
        """
        path = Path(file_path)
        
        if not sequences:
            raise ValidationError("No sequences to write")

        try:
            # Convert to SeqRecord objects
            records = [seq_data.to_seqrecord() for seq_data in sequences]

            # Create output directory if needed
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write using BioPython
            if compress:
                with gzip.open(path, 'wt', encoding='utf-8') as f:
                    SeqIO.write(records, f, format)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    SeqIO.write(records, f, format)

        except Exception as e:
            raise IOError(f"Failed to write sequences to {file_path}: {e}") from e

    def count_sequences(self, sequences: SequenceCollection) -> int:
        """
        Count number of sequences.

        Args:
            sequences: Collection of sequence data

        Returns:
            Number of sequences
        """
        return len(sequences)

    def get_total_length(self, sequences: SequenceCollection) -> int:
        """
        Get total length of all sequences.

        Args:
            sequences: Collection of sequence data

        Returns:
            Total sequence length
        """
        return sum(seq_data.length for seq_data in sequences) 