"""
QZA file reader for the microflex library.

This module provides functionality to read QZA (QIIME2 artifact) files
and extract their contents.
"""

import json
import zipfile
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List
import uuid

import pandas as pd

from microflex.core.exceptions import IOError, ValidationError, DependencyError
from microflex.core.types import FilePath


class QzaReader:
    """
    Reader for QZA (QIIME2 artifact) files.

    This class handles reading QZA files and extracting their contents
    without requiring a full QIIME2 installation.
    """

    def __init__(self) -> None:
        """Initialize QZA reader."""
        pass

    def read(self, file_path: FilePath) -> Dict[str, Any]:
        """
        Read QZA file and return structured data.

        Args:
            file_path: Path to the QZA file

        Returns:
            Dictionary containing QZA data and metadata

        Raises:
            IOError: If file cannot be read
            ValidationError: If file format is invalid
        """
        path = Path(file_path)
        
        if not path.exists():
            raise IOError(f"File not found: {file_path}")

        if not self.validate_format(file_path):
            raise ValidationError(f"Invalid QZA format: {file_path}")

        try:
            return self._parse_qza(path)
        except Exception as e:
            raise IOError(f"Failed to read QZA file {file_path}: {e}") from e

    def _parse_qza(self, path: Path) -> Dict[str, Any]:
        """
        Parse QZA file and return structured data.

        Args:
            path: Path to the QZA file

        Returns:
            Dictionary containing QZA data and metadata
        """
        result = {
            'source_file': str(path),
            'format': 'qza',
        }

        with zipfile.ZipFile(path, 'r') as zf:
            # Read metadata
            try:
                with zf.open('metadata.yaml') as f:
                    metadata_content = f.read().decode('utf-8')
                    result['metadata_yaml'] = metadata_content
                    
                    # Try to parse YAML if available
                    try:
                        import yaml
                        metadata = yaml.safe_load(metadata_content)
                        result['metadata'] = metadata
                    except ImportError:
                        result['metadata'] = {'note': 'Install PyYAML to parse metadata'}
                        
            except KeyError:
                result['metadata'] = {}

            # Read provenance
            try:
                provenance_files = [name for name in zf.namelist() if name.startswith('provenance/')]
                result['provenance_files'] = provenance_files
                
                # Read action.yaml if present
                action_file = 'provenance/action/action.yaml'
                if action_file in zf.namelist():
                    with zf.open(action_file) as f:
                        action_content = f.read().decode('utf-8')
                        result['action_yaml'] = action_content
                        
            except Exception:
                result['provenance_files'] = []

            # Extract data files
            data_files = [name for name in zf.namelist() if name.startswith('data/')]
            result['data_files'] = data_files

            # Try to extract and parse common data formats
            result['data'] = self._extract_data_files(zf, data_files)

        return result

    def _extract_data_files(self, zf: zipfile.ZipFile, data_files: List[str]) -> Dict[str, Any]:
        """
        Extract and parse data files from QZA archive.

        Args:
            zf: ZipFile object
            data_files: List of data file paths

        Returns:
            Dictionary containing parsed data
        """
        data = {}

        for file_path in data_files:
            file_name = Path(file_path).name
            
            try:
                with zf.open(file_path) as f:
                    content = f.read()

                # Try to parse based on file extension
                if file_name.endswith('.tsv') or file_name.endswith('.txt'):
                    try:
                        # Try to parse as TSV
                        content_str = content.decode('utf-8')
                        lines = content_str.strip().split('\n')
                        if lines:
                            # Check if it looks like a table
                            first_line = lines[0]
                            if '\t' in first_line:
                                # Parse as DataFrame
                                from io import StringIO
                                df = pd.read_csv(StringIO(content_str), sep='\t')
                                data[file_name] = df
                            else:
                                data[file_name] = content_str
                    except Exception:
                        data[file_name] = content.decode('utf-8', errors='ignore')

                elif file_name.endswith('.biom'):
                    # BIOM file - store raw content for now
                    data[file_name] = content

                elif file_name.endswith('.fasta') or file_name.endswith('.fa'):
                    # FASTA file
                    data[file_name] = content.decode('utf-8', errors='ignore')

                elif file_name.endswith('.fastq') or file_name.endswith('.fq'):
                    # FASTQ file
                    data[file_name] = content.decode('utf-8', errors='ignore')

                elif file_name.endswith('.json'):
                    # JSON file
                    try:
                        json_data = json.loads(content.decode('utf-8'))
                        data[file_name] = json_data
                    except json.JSONDecodeError:
                        data[file_name] = content.decode('utf-8', errors='ignore')

                else:
                    # Unknown format - store as bytes
                    data[file_name] = content

            except Exception as e:
                data[file_name] = f"Error reading file: {e}"

        return data

    def validate_format(self, file_path: FilePath) -> bool:
        """
        Validate if file is in QZA format.

        Args:
            file_path: Path to the file

        Returns:
            True if file is valid QZA, False otherwise
        """
        path = Path(file_path)
        
        if not path.exists():
            return False

        # Check file extension
        if path.suffix.lower() != '.qza':
            return False

        try:
            # Check if it's a valid ZIP file
            with zipfile.ZipFile(path, 'r') as zf:
                # Check for required QZA structure
                file_list = zf.namelist()
                
                # QZA files should have metadata.yaml and data/ directory
                has_metadata = any(name == 'metadata.yaml' for name in file_list)
                has_data_dir = any(name.startswith('data/') for name in file_list)
                
                return has_metadata and has_data_dir

        except (zipfile.BadZipFile, Exception):
            return False

    def extract_to_directory(self, file_path: FilePath, output_dir: FilePath) -> Path:
        """
        Extract QZA contents to a directory.

        Args:
            file_path: Path to the QZA file
            output_dir: Directory to extract contents to

        Returns:
            Path to the extraction directory

        Raises:
            IOError: If extraction fails
        """
        path = Path(file_path)
        output_path = Path(output_dir)
        
        if not path.exists():
            raise IOError(f"File not found: {file_path}")

        if not self.validate_format(file_path):
            raise ValidationError(f"Invalid QZA format: {file_path}")

        try:
            # Create output directory
            extract_dir = output_path / f"{path.stem}_extracted"
            extract_dir.mkdir(parents=True, exist_ok=True)

            # Extract ZIP contents
            with zipfile.ZipFile(path, 'r') as zf:
                zf.extractall(extract_dir)

            return extract_dir

        except Exception as e:
            raise IOError(f"Failed to extract QZA file {file_path}: {e}") from e

    def get_artifact_type(self, file_path: FilePath) -> Optional[str]:
        """
        Get the artifact type from QZA metadata.

        Args:
            file_path: Path to the QZA file

        Returns:
            Artifact type string or None if not found

        Raises:
            IOError: If file cannot be read
        """
        try:
            qza_data = self.read(file_path)
            metadata = qza_data.get('metadata', {})
            
            if isinstance(metadata, dict):
                return metadata.get('type')
            
            return None

        except Exception as e:
            raise IOError(f"Failed to get artifact type from {file_path}: {e}") from e

    def get_uuid(self, file_path: FilePath) -> Optional[str]:
        """
        Get the UUID from QZA metadata.

        Args:
            file_path: Path to the QZA file

        Returns:
            UUID string or None if not found

        Raises:
            IOError: If file cannot be read
        """
        try:
            qza_data = self.read(file_path)
            metadata = qza_data.get('metadata', {})
            
            if isinstance(metadata, dict):
                return metadata.get('uuid')
            
            return None

        except Exception as e:
            raise IOError(f"Failed to get UUID from {file_path}: {e}") from e

    def list_data_files(self, file_path: FilePath) -> List[str]:
        """
        List all data files in the QZA archive.

        Args:
            file_path: Path to the QZA file

        Returns:
            List of data file paths

        Raises:
            IOError: If file cannot be read
        """
        try:
            qza_data = self.read(file_path)
            return qza_data.get('data_files', [])

        except Exception as e:
            raise IOError(f"Failed to list data files from {file_path}: {e}") from e 