"""
BIOM file reader for the microflex library.

This module provides functionality to read BIOM format files
and convert them to the internal data structures.
"""

import json
import gzip
from pathlib import Path
from typing import Dict, List, Any, Optional

import pandas as pd
import numpy as np

from microflex.core.exceptions import IOError, ValidationError, DependencyError
from microflex.core.types import (
    TaxonomyResult,
    TaxonomyCollection,
    FilePath,
)


class BiomReader:
    """
    Reader for BIOM format files.

    This class handles reading BIOM files (both JSON and HDF5 formats)
    and converts them to internal data structures.
    """

    def __init__(self) -> None:
        """Initialize BIOM reader."""
        pass

    def read(self, file_path: FilePath) -> Dict[str, Any]:
        """
        Read BIOM file and return structured data.

        Args:
            file_path: Path to the BIOM file

        Returns:
            Dictionary containing BIOM data

        Raises:
            IOError: If file cannot be read
            ValidationError: If file format is invalid
        """
        path = Path(file_path)
        
        if not path.exists():
            raise IOError(f"File not found: {file_path}")

        if not self.validate_format(file_path):
            raise ValidationError(f"Invalid BIOM format: {file_path}")

        try:
            return self._parse_biom(path)
        except Exception as e:
            raise IOError(f"Failed to read BIOM file {file_path}: {e}") from e

    def _parse_biom(self, path: Path) -> Dict[str, Any]:
        """
        Parse BIOM file and return structured data.

        Args:
            path: Path to the BIOM file

        Returns:
            Dictionary containing BIOM data
        """
        # Check if file is compressed
        is_compressed = path.suffix.lower() == '.gz'
        
        try:
            if is_compressed:
                with gzip.open(path, 'rt', encoding='utf-8') as f:
                    content = f.read()
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

            # Try to parse as JSON first (BIOM 1.0 format)
            try:
                biom_data = json.loads(content)
                return self._parse_biom_json(biom_data, path)
            except json.JSONDecodeError:
                # Might be HDF5 format (BIOM 2.0+)
                return self._parse_biom_hdf5(path)

        except Exception as e:
            raise IOError(f"Failed to parse BIOM file: {e}") from e

    def _parse_biom_json(self, biom_data: Dict[str, Any], path: Path) -> Dict[str, Any]:
        """
        Parse JSON-format BIOM data.

        Args:
            biom_data: Parsed JSON data
            path: Original file path

        Returns:
            Structured BIOM data
        """
        # Extract basic information
        result = {
            'format': 'biom_json',
            'format_version': biom_data.get('format_version', '1.0'),
            'id': biom_data.get('id', path.stem),
            'type': biom_data.get('type', 'OTU table'),
            'generated_by': biom_data.get('generated_by', 'unknown'),
            'creation_date': biom_data.get('date', ''),
            'source_file': str(path),
        }

        # Extract matrix data
        if 'data' in biom_data:
            matrix_data = biom_data['data']
            shape = biom_data.get('shape', [0, 0])
            
            # Convert sparse matrix to dense if needed
            if biom_data.get('matrix_type') == 'sparse':
                dense_matrix = np.zeros(shape)
                for row, col, value in matrix_data:
                    dense_matrix[row, col] = value
                result['matrix'] = dense_matrix
            else:
                result['matrix'] = np.array(matrix_data)

        # Extract sample metadata
        if 'columns' in biom_data:
            samples = []
            for col_data in biom_data['columns']:
                sample = {
                    'id': col_data['id'],
                    'metadata': col_data.get('metadata', {})
                }
                samples.append(sample)
            result['samples'] = samples

        # Extract observation (OTU/feature) metadata
        if 'rows' in biom_data:
            observations = []
            for row_data in biom_data['rows']:
                obs = {
                    'id': row_data['id'],
                    'metadata': row_data.get('metadata', {})
                }
                observations.append(obs)
            result['observations'] = observations

        return result

    def _parse_biom_hdf5(self, path: Path) -> Dict[str, Any]:
        """
        Parse HDF5-format BIOM data.

        Args:
            path: Path to HDF5 BIOM file

        Returns:
            Structured BIOM data

        Note:
            Requires h5py for full functionality
        """
        try:
            import h5py
            
            with h5py.File(path, 'r') as f:
                result = {
                    'format': 'biom_hdf5',
                    'source_file': str(path),
                }
                
                # Extract basic attributes
                if 'id' in f.attrs:
                    result['id'] = f.attrs['id'].decode('utf-8')
                if 'type' in f.attrs:
                    result['type'] = f.attrs['type'].decode('utf-8')
                if 'format-version' in f.attrs:
                    result['format_version'] = f.attrs['format-version'].decode('utf-8')

                # Extract matrix data
                if 'observation' in f and 'matrix' in f['observation']:
                    matrix_group = f['observation']['matrix']
                    if 'data' in matrix_group:
                        # Sparse matrix format
                        data = matrix_group['data'][:]
                        indices = matrix_group['indices'][:]
                        indptr = matrix_group['indptr'][:]
                        shape = matrix_group.attrs['shape']
                        
                        # Convert to dense matrix
                        from scipy.sparse import csr_matrix
                        sparse_matrix = csr_matrix((data, indices, indptr), shape=shape)
                        result['matrix'] = sparse_matrix.toarray()

                # Extract sample IDs
                if 'sample' in f and 'ids' in f['sample']:
                    sample_ids = [id.decode('utf-8') for id in f['sample']['ids'][:]]
                    result['sample_ids'] = sample_ids

                # Extract observation IDs
                if 'observation' in f and 'ids' in f['observation']:
                    obs_ids = [id.decode('utf-8') for id in f['observation']['ids'][:]]
                    result['observation_ids'] = obs_ids

                return result

        except ImportError:
            raise DependencyError(
                "h5py is required for HDF5 BIOM files. "
                "Install with: pip install h5py"
            )
        except Exception as e:
            raise IOError(f"Failed to parse HDF5 BIOM file: {e}") from e

    def validate_format(self, file_path: FilePath) -> bool:
        """
        Validate if file is in BIOM format.

        Args:
            file_path: Path to the file

        Returns:
            True if file is valid BIOM, False otherwise
        """
        path = Path(file_path)
        
        if not path.exists():
            return False

        try:
            # Check file extension
            if path.suffix.lower() not in ['.biom', '.gz']:
                return False

            # Check if compressed
            is_compressed = path.suffix.lower() == '.gz'
            
            if is_compressed:
                with gzip.open(path, 'rt', encoding='utf-8') as f:
                    first_line = f.readline().strip()
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()

            # Check for JSON BIOM format
            if first_line.startswith('{'):
                try:
                    if is_compressed:
                        with gzip.open(path, 'rt', encoding='utf-8') as f:
                            data = json.load(f)
                    else:
                        with open(path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    
                    # Check for BIOM-specific fields
                    return 'format' in data or 'type' in data or 'matrix_type' in data
                except json.JSONDecodeError:
                    pass

            # Check for HDF5 BIOM format
            try:
                import h5py
                with h5py.File(path, 'r') as f:
                    # Check for BIOM-specific structure
                    return 'observation' in f or 'sample' in f
            except (ImportError, Exception):
                pass

            return False

        except Exception:
            return False

    def to_taxonomy_results(self, biom_data: Dict[str, Any]) -> TaxonomyCollection:
        """
        Convert BIOM observation metadata to taxonomy results.

        Args:
            biom_data: Parsed BIOM data

        Returns:
            Collection of taxonomy results
        """
        taxonomy_results = []
        
        if 'observations' in biom_data:
            for obs in biom_data['observations']:
                obs_id = obs['id']
                metadata = obs.get('metadata', {})
                
                # Extract taxonomy information
                taxonomy = metadata.get('taxonomy', [])
                if isinstance(taxonomy, str):
                    taxonomy = taxonomy.split(';')
                
                # Create taxonomy result
                tax_result = TaxonomyResult(
                    sequence_id=obs_id,
                    kingdom=taxonomy[0] if len(taxonomy) > 0 else None,
                    phylum=taxonomy[1] if len(taxonomy) > 1 else None,
                    class_=taxonomy[2] if len(taxonomy) > 2 else None,
                    order=taxonomy[3] if len(taxonomy) > 3 else None,
                    family=taxonomy[4] if len(taxonomy) > 4 else None,
                    genus=taxonomy[5] if len(taxonomy) > 5 else None,
                    species=taxonomy[6] if len(taxonomy) > 6 else None,
                    confidence=metadata.get('confidence'),
                    method='biom_import',
                    metadata=metadata
                )
                
                taxonomy_results.append(tax_result)
        
        return taxonomy_results

    def to_dataframe(self, biom_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Convert BIOM data to pandas DataFrame.

        Args:
            biom_data: Parsed BIOM data

        Returns:
            DataFrame with samples as columns and observations as rows
        """
        if 'matrix' not in biom_data:
            return pd.DataFrame()

        matrix = biom_data['matrix']
        
        # Get sample and observation IDs
        sample_ids = biom_data.get('sample_ids', [f'Sample_{i}' for i in range(matrix.shape[1])])
        obs_ids = biom_data.get('observation_ids', [f'OTU_{i}' for i in range(matrix.shape[0])])
        
        # Create DataFrame
        df = pd.DataFrame(matrix, index=obs_ids, columns=sample_ids)
        return df 