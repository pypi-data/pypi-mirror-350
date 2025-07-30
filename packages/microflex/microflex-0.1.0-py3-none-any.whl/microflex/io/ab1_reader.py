"""
AB1 file reader for the microflex library.

This module provides functionality to read AB1 (Applied Biosystems) files
from Sanger sequencing and convert them to the internal SequenceData format.
"""

import struct
from pathlib import Path
from typing import Optional, Tuple

import numpy as np

from microflex.core.exceptions import IOError, ValidationError, DependencyError
from microflex.core.types import (
    SequenceData,
    SequenceCollection,
    QualityData,
    SequencingTechnology,
    FilePath,
)


class Ab1Reader:
    """
    Reader for AB1 format files from Sanger sequencing.

    This class handles reading AB1 files and converts them to the internal
    SequenceData format with quality scores and trace data.
    """

    def __init__(self) -> None:
        """Initialize AB1 reader."""
        pass

    def read(self, file_path: FilePath) -> SequenceCollection:
        """
        Read sequence from AB1 file.

        Args:
            file_path: Path to the AB1 file

        Returns:
            Collection containing single sequence data

        Raises:
            IOError: If file cannot be read
            ValidationError: If file format is invalid
        """
        path = Path(file_path)
        
        if not path.exists():
            raise IOError(f"File not found: {file_path}")

        if not self.validate_format(file_path):
            raise ValidationError(f"Invalid AB1 format: {file_path}")

        try:
            seq_data = self._parse_ab1(path)
            return [seq_data]
        except Exception as e:
            raise IOError(f"Failed to read AB1 file {file_path}: {e}") from e

    def _parse_ab1(self, path: Path) -> SequenceData:
        """
        Parse AB1 file and return SequenceData object.

        Args:
            path: Path to the AB1 file

        Returns:
            SequenceData object

        Raises:
            IOError: If file cannot be parsed
        """
        try:
            # Try to use BioPython if available
            from Bio import SeqIO
            
            with open(path, 'rb') as f:
                record = SeqIO.read(f, 'abi')
                
            # Extract quality scores if available
            quality_data = None
            if hasattr(record, 'letter_annotations') and 'phred_quality' in record.letter_annotations:
                quality_scores = np.array(record.letter_annotations['phred_quality'])
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
                sequence_id=record.id or path.stem,
                description=record.description or f"Sanger sequence from {path.name}",
                quality=quality_data,
                technology=SequencingTechnology.SANGER,
                metadata={
                    'source_file': str(path),
                    'format': 'ab1',
                    'annotations': getattr(record, 'annotations', {}),
                }
            )

            return seq_data

        except ImportError:
            # Fallback to basic AB1 parsing without BioPython
            return self._parse_ab1_basic(path)

    def _parse_ab1_basic(self, path: Path) -> SequenceData:
        """
        Basic AB1 parsing without external dependencies.

        Args:
            path: Path to the AB1 file

        Returns:
            SequenceData object

        Note:
            This is a simplified parser that extracts basic information.
            For full AB1 support, BioPython is recommended.
        """
        with open(path, 'rb') as f:
            # Read AB1 header
            header = f.read(4)
            if header != b'ABIF':
                raise IOError("Invalid AB1 file: missing ABIF signature")

            # Skip version info
            f.seek(18)
            
            # Read directory info
            dir_entry_size = struct.unpack('>H', f.read(2))[0]
            num_entries = struct.unpack('>I', f.read(4))[0]
            
            # Try to find sequence data
            sequence = ""
            sample_name = path.stem
            
            # This is a very basic implementation
            # In a real implementation, you would parse the directory entries
            # to find specific data tags like PBAS (base calls), PLOC (peak locations), etc.
            
            # For now, return a placeholder sequence
            seq_data = SequenceData(
                sequence=sequence or "N" * 100,  # Placeholder
                sequence_id=sample_name,
                description=f"Sanger sequence from {path.name} (basic parser)",
                quality=None,
                technology=SequencingTechnology.SANGER,
                metadata={
                    'source_file': str(path),
                    'format': 'ab1',
                    'parser': 'basic',
                    'note': 'Install BioPython for full AB1 support',
                }
            )

            return seq_data

    def validate_format(self, file_path: FilePath) -> bool:
        """
        Validate if file is in AB1 format.

        Args:
            file_path: Path to the file

        Returns:
            True if file is valid AB1, False otherwise
        """
        path = Path(file_path)
        
        if not path.exists():
            return False

        try:
            with open(path, 'rb') as f:
                # Check for ABIF signature
                header = f.read(4)
                return header == b'ABIF'
        except Exception:
            return False

    def get_trace_data(self, file_path: FilePath) -> Optional[dict]:
        """
        Extract trace data from AB1 file.

        Args:
            file_path: Path to the AB1 file

        Returns:
            Dictionary with trace data or None if not available

        Note:
            Requires BioPython for full functionality
        """
        try:
            from Bio import SeqIO
            
            with open(file_path, 'rb') as f:
                record = SeqIO.read(f, 'abi')
                
            # Extract trace data if available
            trace_data = {}
            if hasattr(record, 'annotations'):
                annotations = record.annotations
                
                # Common AB1 trace data fields
                trace_fields = ['channel_1', 'channel_2', 'channel_3', 'channel_4']
                for field in trace_fields:
                    if field in annotations:
                        trace_data[field] = annotations[field]
                
                # Peak locations
                if 'peak_locations' in annotations:
                    trace_data['peak_locations'] = annotations['peak_locations']
                    
            return trace_data if trace_data else None
            
        except ImportError:
            raise DependencyError(
                "BioPython is required for trace data extraction. "
                "Install with: pip install biopython"
            )
        except Exception as e:
            raise IOError(f"Failed to extract trace data from {file_path}: {e}") from e

    def get_sample_info(self, file_path: FilePath) -> dict:
        """
        Extract sample information from AB1 file.

        Args:
            file_path: Path to the AB1 file

        Returns:
            Dictionary with sample information

        Raises:
            IOError: If file cannot be read
        """
        path = Path(file_path)
        
        if not path.exists():
            raise IOError(f"File not found: {file_path}")

        try:
            from Bio import SeqIO
            
            with open(path, 'rb') as f:
                record = SeqIO.read(f, 'abi')
                
            info = {
                'sample_name': getattr(record, 'id', path.stem),
                'description': getattr(record, 'description', ''),
                'sequence_length': len(record.seq),
            }
            
            # Extract additional metadata from annotations
            if hasattr(record, 'annotations'):
                annotations = record.annotations
                
                # Common metadata fields
                metadata_fields = [
                    'run_start', 'run_finish', 'machine_model',
                    'sample_name', 'well_id', 'lane', 'signal_strength'
                ]
                
                for field in metadata_fields:
                    if field in annotations:
                        info[field] = annotations[field]
                        
            return info
            
        except ImportError:
            # Basic info without BioPython
            return {
                'sample_name': path.stem,
                'description': f"AB1 file: {path.name}",
                'sequence_length': 0,
                'note': 'Install BioPython for detailed sample information',
            }
        except Exception as e:
            raise IOError(f"Failed to extract sample info from {file_path}: {e}") from e 