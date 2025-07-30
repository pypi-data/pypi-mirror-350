"""
Taxonomy writer for the microflex library.

This module provides functionality to write taxonomic classification results
to various formats including TSV, CSV, and BIOM.
"""

import json
import gzip
from pathlib import Path
from typing import Optional, TextIO, Dict, Any

import pandas as pd

from microflex.core.exceptions import IOError, ValidationError
from microflex.core.types import (
    TaxonomyResult,
    TaxonomyCollection,
    FileFormat,
    FilePath,
)


class TaxonomyWriter:
    """
    Writer for taxonomic classification results.

    This class handles writing TaxonomyResult objects to files in
    various formats including TSV, CSV, and BIOM.
    """

    def __init__(self) -> None:
        """Initialize taxonomy writer."""
        pass

    def write(
        self,
        taxonomy_results: TaxonomyCollection,
        file_path: FilePath,
        format: Optional[FileFormat] = None,
        compress: bool = False,
        **kwargs
    ) -> None:
        """
        Write taxonomy results to file.

        Args:
            taxonomy_results: Collection of taxonomy results
            file_path: Path to output file
            format: Output format (auto-detected if None)
            compress: Whether to compress output with gzip
            **kwargs: Additional format-specific parameters

        Raises:
            IOError: If file cannot be written
            ValidationError: If format is not supported
        """
        path = Path(file_path)
        
        if not taxonomy_results:
            raise ValidationError("No taxonomy results to write")

        # Auto-detect format if not specified
        if format is None:
            format = self._detect_format_from_path(path)

        # Validate format
        supported_formats = [FileFormat.TSV, FileFormat.CSV, FileFormat.BIOM]
        if format not in supported_formats:
            raise ValidationError(f"Unsupported output format: {format}")

        try:
            # Create output directory if needed
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write taxonomy results
            if format == FileFormat.BIOM:
                self._write_biom(taxonomy_results, path, compress, **kwargs)
            else:
                if compress:
                    with gzip.open(path, 'wt', encoding='utf-8') as f:
                        self._write_tabular(f, taxonomy_results, format, **kwargs)
                else:
                    with open(path, 'w', encoding='utf-8') as f:
                        self._write_tabular(f, taxonomy_results, format, **kwargs)

        except Exception as e:
            raise IOError(f"Failed to write taxonomy results to {file_path}: {e}") from e

    def _write_tabular(
        self,
        file_handle: TextIO,
        taxonomy_results: TaxonomyCollection,
        format: FileFormat,
        include_confidence: bool = True,
        include_metadata: bool = False,
        **kwargs
    ) -> None:
        """
        Write taxonomy results in tabular format (TSV/CSV).

        Args:
            file_handle: File handle to write to
            taxonomy_results: Collection of taxonomy results
            format: Output format (TSV or CSV)
            include_confidence: Whether to include confidence scores
            include_metadata: Whether to include metadata columns
            **kwargs: Additional parameters
        """
        # Determine separator
        separator = '\t' if format == FileFormat.TSV else ','

        # Define columns
        columns = [
            'sequence_id',
            'kingdom',
            'phylum',
            'class',
            'order',
            'family',
            'genus',
            'species'
        ]

        if include_confidence:
            columns.append('confidence')

        # Add method and database columns
        columns.extend(['method', 'database'])

        # Write header
        file_handle.write(separator.join(columns) + '\n')

        # Write data rows
        for result in taxonomy_results:
            row = [
                result.sequence_id or '',
                result.kingdom or '',
                result.phylum or '',
                result.class_ or '',
                result.order or '',
                result.family or '',
                result.genus or '',
                result.species or ''
            ]

            if include_confidence:
                row.append(str(result.confidence) if result.confidence is not None else '')

            row.extend([
                result.method or '',
                result.database or ''
            ])

            # Handle CSV escaping
            if format == FileFormat.CSV:
                row = [f'"{field}"' if separator in field else field for field in row]

            file_handle.write(separator.join(row) + '\n')

    def _write_biom(
        self,
        taxonomy_results: TaxonomyCollection,
        file_path: Path,
        compress: bool = False,
        **kwargs
    ) -> None:
        """
        Write taxonomy results in BIOM format.

        Args:
            taxonomy_results: Collection of taxonomy results
            file_path: Path to output file
            compress: Whether to compress output
            **kwargs: Additional parameters
        """
        # Create BIOM structure
        biom_data = {
            "id": file_path.stem,
            "format": "Biological Observation Matrix 1.0.0",
            "format_version": [1, 0, 0],
            "type": "OTU table",
            "generated_by": "microflex",
            "date": pd.Timestamp.now().isoformat(),
            "matrix_type": "sparse",
            "matrix_element_type": "int",
            "shape": [len(taxonomy_results), 1],  # Single sample
            "data": [],
            "rows": [],
            "columns": [{"id": "sample_1", "metadata": None}]
        }

        # Add observation data
        for i, result in enumerate(taxonomy_results):
            # Add matrix data (assuming count of 1 for each OTU)
            biom_data["data"].append([i, 0, 1])

            # Add observation metadata
            taxonomy_list = [
                result.kingdom,
                result.phylum,
                result.class_,
                result.order,
                result.family,
                result.genus,
                result.species
            ]

            # Remove None values and create taxonomy string
            taxonomy_clean = [tax for tax in taxonomy_list if tax is not None]

            observation = {
                "id": result.sequence_id,
                "metadata": {
                    "taxonomy": taxonomy_clean
                }
            }

            # Add confidence if available
            if result.confidence is not None:
                observation["metadata"]["confidence"] = result.confidence

            # Add method and database info
            if result.method:
                observation["metadata"]["method"] = result.method
            if result.database:
                observation["metadata"]["database"] = result.database

            biom_data["rows"].append(observation)

        # Write BIOM file
        if compress:
            with gzip.open(file_path, 'wt', encoding='utf-8') as f:
                json.dump(biom_data, f, indent=2)
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(biom_data, f, indent=2)

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
            '.tsv': FileFormat.TSV,
            '.txt': FileFormat.TSV,
            '.csv': FileFormat.CSV,
            '.biom': FileFormat.BIOM,
        }

        if suffix in format_map:
            return format_map[suffix]

        # Default to TSV if cannot detect
        return FileFormat.TSV

    def write_tsv(
        self,
        taxonomy_results: TaxonomyCollection,
        file_path: FilePath,
        compress: bool = False,
        **kwargs
    ) -> None:
        """
        Write taxonomy results in TSV format.

        Args:
            taxonomy_results: Collection of taxonomy results
            file_path: Path to output file
            compress: Whether to compress output with gzip
            **kwargs: Additional parameters

        Raises:
            IOError: If file cannot be written
        """
        self.write(
            taxonomy_results,
            file_path,
            format=FileFormat.TSV,
            compress=compress,
            **kwargs
        )

    def write_csv(
        self,
        taxonomy_results: TaxonomyCollection,
        file_path: FilePath,
        compress: bool = False,
        **kwargs
    ) -> None:
        """
        Write taxonomy results in CSV format.

        Args:
            taxonomy_results: Collection of taxonomy results
            file_path: Path to output file
            compress: Whether to compress output with gzip
            **kwargs: Additional parameters

        Raises:
            IOError: If file cannot be written
        """
        self.write(
            taxonomy_results,
            file_path,
            format=FileFormat.CSV,
            compress=compress,
            **kwargs
        )

    def write_biom(
        self,
        taxonomy_results: TaxonomyCollection,
        file_path: FilePath,
        compress: bool = False,
        **kwargs
    ) -> None:
        """
        Write taxonomy results in BIOM format.

        Args:
            taxonomy_results: Collection of taxonomy results
            file_path: Path to output file
            compress: Whether to compress output with gzip
            **kwargs: Additional parameters

        Raises:
            IOError: If file cannot be written
        """
        self.write(
            taxonomy_results,
            file_path,
            format=FileFormat.BIOM,
            compress=compress,
            **kwargs
        )

    def to_dataframe(self, taxonomy_results: TaxonomyCollection) -> pd.DataFrame:
        """
        Convert taxonomy results to pandas DataFrame.

        Args:
            taxonomy_results: Collection of taxonomy results

        Returns:
            DataFrame with taxonomy data
        """
        if not taxonomy_results:
            return pd.DataFrame()

        data = []
        for result in taxonomy_results:
            row = {
                'sequence_id': result.sequence_id,
                'kingdom': result.kingdom,
                'phylum': result.phylum,
                'class': result.class_,
                'order': result.order,
                'family': result.family,
                'genus': result.genus,
                'species': result.species,
                'confidence': result.confidence,
                'method': result.method,
                'database': result.database,
                'full_taxonomy': result.full_taxonomy,
                'lowest_classification': result.lowest_classification
            }
            data.append(row)

        return pd.DataFrame(data)

    def write_dataframe(
        self,
        taxonomy_results: TaxonomyCollection,
        file_path: FilePath,
        format: Optional[FileFormat] = None,
        **kwargs
    ) -> None:
        """
        Write taxonomy results using pandas DataFrame.

        Args:
            taxonomy_results: Collection of taxonomy results
            file_path: Path to output file
            format: Output format (auto-detected if None)
            **kwargs: Additional pandas parameters

        Raises:
            IOError: If file cannot be written
        """
        df = self.to_dataframe(taxonomy_results)
        
        if df.empty:
            raise ValidationError("No taxonomy results to write")

        path = Path(file_path)
        
        # Auto-detect format if not specified
        if format is None:
            format = self._detect_format_from_path(path)

        try:
            # Create output directory if needed
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write using pandas
            if format == FileFormat.CSV:
                df.to_csv(path, index=False, **kwargs)
            else:  # TSV
                df.to_csv(path, sep='\t', index=False, **kwargs)

        except Exception as e:
            raise IOError(f"Failed to write taxonomy results to {file_path}: {e}") from e 