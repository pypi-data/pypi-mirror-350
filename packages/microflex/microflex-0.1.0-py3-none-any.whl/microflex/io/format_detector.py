"""
File format detection for the microflex library.

This module provides automatic detection of file formats based on
file extensions, magic numbers, and content analysis.
"""

import gzip
import zipfile
from pathlib import Path
from typing import Optional

from microflex.core.exceptions import IOError
from microflex.core.types import FileFormat, FilePath


class FormatDetector:
    """
    Automatic file format detection.

    This class analyzes files to determine their format based on
    file extensions, magic numbers, and content structure.
    """

    # File extension mappings
    EXTENSION_MAP = {
        '.fastq': FileFormat.FASTQ,
        '.fq': FileFormat.FASTQ,
        '.fasta': FileFormat.FASTA,
        '.fa': FileFormat.FASTA,
        '.fas': FileFormat.FASTA,
        '.ab1': FileFormat.AB1,
        '.abi': FileFormat.AB1,
        '.qza': FileFormat.QZA,
        '.biom': FileFormat.BIOM,
        '.tsv': FileFormat.TSV,
        '.txt': FileFormat.TSV,
        '.csv': FileFormat.CSV,
    }

    # Magic number signatures
    MAGIC_NUMBERS = {
        b'ABIF': FileFormat.AB1,
        b'PK': FileFormat.QZA,  # ZIP-based format
        b'\x1f\x8b': 'gzip',  # Gzipped file
    }

    @classmethod
    def detect_format(cls, file_path: FilePath) -> FileFormat:
        """
        Detect file format automatically.

        Args:
            file_path: Path to the file

        Returns:
            Detected file format

        Raises:
            IOError: If format cannot be detected or file doesn't exist
        """
        path = Path(file_path)
        
        if not path.exists():
            raise IOError(f"File not found: {file_path}")

        # First try extension-based detection
        format_from_ext = cls._detect_from_extension(path)
        if format_from_ext:
            return format_from_ext

        # Then try magic number detection
        format_from_magic = cls._detect_from_magic_number(path)
        if format_from_magic:
            return format_from_magic

        # Finally try content-based detection
        format_from_content = cls._detect_from_content(path)
        if format_from_content:
            return format_from_content

        raise IOError(f"Cannot detect format for file: {file_path}")

    @classmethod
    def _detect_from_extension(cls, path: Path) -> Optional[FileFormat]:
        """
        Detect format from file extension.

        Args:
            path: File path

        Returns:
            Detected format or None
        """
        # Handle compressed files
        if path.suffix.lower() == '.gz':
            # Check the extension before .gz
            stem_path = Path(path.stem)
            if stem_path.suffix.lower() in cls.EXTENSION_MAP:
                return cls.EXTENSION_MAP[stem_path.suffix.lower()]
        
        # Check direct extension mapping
        if path.suffix.lower() in cls.EXTENSION_MAP:
            return cls.EXTENSION_MAP[path.suffix.lower()]

        return None

    @classmethod
    def _detect_from_magic_number(cls, path: Path) -> Optional[FileFormat]:
        """
        Detect format from magic numbers.

        Args:
            path: File path

        Returns:
            Detected format or None
        """
        try:
            with open(path, 'rb') as f:
                header = f.read(8)
                
                for magic, format_type in cls.MAGIC_NUMBERS.items():
                    if header.startswith(magic):
                        if format_type == 'gzip':
                            # For gzipped files, try to detect the underlying format
                            return cls._detect_gzipped_format(path)
                        return format_type

        except Exception:
            pass

        return None

    @classmethod
    def _detect_from_content(cls, path: Path) -> Optional[FileFormat]:
        """
        Detect format from file content.

        Args:
            path: File path

        Returns:
            Detected format or None
        """
        try:
            # Try to read as text first
            with open(path, 'r', encoding='utf-8') as f:
                first_lines = [f.readline().strip() for _ in range(5)]
                
            # Check for FASTA format
            if any(line.startswith('>') for line in first_lines):
                return FileFormat.FASTA

            # Check for FASTQ format
            if len(first_lines) >= 4:
                if (first_lines[0].startswith('@') and 
                    first_lines[2].startswith('+') and
                    len(first_lines[1]) == len(first_lines[3])):
                    return FileFormat.FASTQ

            # Check for TSV/CSV format
            if any('\t' in line for line in first_lines):
                return FileFormat.TSV
            elif any(',' in line for line in first_lines):
                return FileFormat.CSV

            # Check for BIOM format (JSON-based)
            content = ''.join(first_lines)
            if content.strip().startswith('{') and 'biom' in content.lower():
                return FileFormat.BIOM

        except UnicodeDecodeError:
            # File is binary, might be AB1
            try:
                with open(path, 'rb') as f:
                    content = f.read(100)
                    if b'ABIF' in content:
                        return FileFormat.AB1
            except Exception:
                pass

        return None

    @classmethod
    def _detect_gzipped_format(cls, path: Path) -> Optional[FileFormat]:
        """
        Detect format of gzipped file.

        Args:
            path: Path to gzipped file

        Returns:
            Detected format or None
        """
        try:
            with gzip.open(path, 'rt', encoding='utf-8') as f:
                first_lines = [f.readline().strip() for _ in range(5)]

            # Check for FASTA format
            if any(line.startswith('>') for line in first_lines):
                return FileFormat.FASTA

            # Check for FASTQ format
            if len(first_lines) >= 4:
                if (first_lines[0].startswith('@') and 
                    first_lines[2].startswith('+') and
                    len(first_lines[1]) == len(first_lines[3])):
                    return FileFormat.FASTQ

        except Exception:
            pass

        return None

    @classmethod
    def is_compressed(cls, file_path: FilePath) -> bool:
        """
        Check if file is compressed.

        Args:
            file_path: Path to the file

        Returns:
            True if file is compressed, False otherwise
        """
        path = Path(file_path)
        
        # Check extension
        if path.suffix.lower() in ['.gz', '.bz2', '.xz']:
            return True

        # Check magic number
        try:
            with open(path, 'rb') as f:
                header = f.read(4)
                return (header.startswith(b'\x1f\x8b') or  # gzip
                        header.startswith(b'BZ') or        # bzip2
                        header.startswith(b'\xfd7zXZ'))    # xz
        except Exception:
            return False

    @classmethod
    def get_supported_formats(cls) -> list[FileFormat]:
        """
        Get list of supported file formats.

        Returns:
            List of supported formats
        """
        return list(set(cls.EXTENSION_MAP.values())) 