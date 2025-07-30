"""
Configuration management for the microflex library.

This module provides configuration handling, validation, and default settings
for all components in the microflex library.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field, validator

from microflex.core.exceptions import ConfigurationError
from microflex.core.types import FilePath


class ProcessingConfig(BaseModel):
    """Configuration for data processing operations."""

    min_length: int = Field(default=100, ge=1, description="Minimum sequence length")
    max_length: Optional[int] = Field(default=None, ge=1, description="Maximum sequence length")
    min_quality: float = Field(default=20.0, ge=0.0, le=50.0, description="Minimum quality score")
    trim_ends: bool = Field(default=True, description="Whether to trim sequence ends")
    remove_chimeras: bool = Field(default=True, description="Whether to remove chimeric sequences")

    @validator('max_length')
    def validate_max_length(cls, v: Optional[int], values: Dict[str, Any]) -> Optional[int]:
        """Validate that max_length is greater than min_length."""
        if v is not None and 'min_length' in values and v <= values['min_length']:
            raise ValueError('max_length must be greater than min_length')
        return v


class ClassificationConfig(BaseModel):
    """Configuration for taxonomic classification."""

    database: str = Field(description="Reference database name or path")
    method: str = Field(default="blast", description="Classification method")
    evalue: float = Field(default=1e-5, ge=0.0, description="E-value threshold")
    identity_threshold: float = Field(default=0.97, ge=0.0, le=1.0, description="Identity threshold")
    coverage_threshold: float = Field(default=0.8, ge=0.0, le=1.0, description="Coverage threshold")
    max_hits: int = Field(default=10, ge=1, description="Maximum number of hits to consider")


class AnalysisConfig(BaseModel):
    """Configuration for diversity analysis."""

    rarefaction_depth: Optional[int] = Field(default=None, ge=1, description="Rarefaction depth")
    alpha_metrics: list[str] = Field(
        default=["shannon", "simpson", "chao1"],
        description="Alpha diversity metrics to calculate"
    )
    beta_metrics: list[str] = Field(
        default=["bray_curtis", "jaccard"],
        description="Beta diversity metrics to calculate"
    )
    ordination_method: str = Field(default="pcoa", description="Ordination method")


class VisualizationConfig(BaseModel):
    """Configuration for visualization."""

    figure_format: str = Field(default="png", description="Output figure format")
    figure_dpi: int = Field(default=300, ge=72, description="Figure DPI")
    figure_width: float = Field(default=10.0, gt=0.0, description="Figure width in inches")
    figure_height: float = Field(default=8.0, gt=0.0, description="Figure height in inches")
    color_palette: str = Field(default="Set1", description="Color palette for plots")
    interactive: bool = Field(default=False, description="Whether to create interactive plots")


class Config:
    """
    Main configuration class for the microflex library.

    This class manages all configuration settings and provides methods
    for loading, saving, and validating configurations.
    """

    def __init__(self, config_file: Optional[FilePath] = None) -> None:
        """
        Initialize configuration.

        Args:
            config_file: Optional path to configuration file
        """
        self.processing = ProcessingConfig()
        self.classification = ClassificationConfig(database="16S_ribosomal_RNA")
        self.analysis = AnalysisConfig()
        self.visualization = VisualizationConfig()
        
        # Load from file if provided
        if config_file:
            self.load_from_file(config_file)

    def load_from_file(self, config_file: FilePath) -> None:
        """
        Load configuration from file.

        Args:
            config_file: Path to configuration file

        Raises:
            ConfigurationError: If file cannot be loaded or is invalid
        """
        config_path = Path(config_file)
        
        if not config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_file}")

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix.lower() == '.json':
                    config_data = json.load(f)
                else:
                    # Assume YAML format
                    try:
                        import yaml
                        config_data = yaml.safe_load(f)
                    except ImportError:
                        raise ConfigurationError(
                            "PyYAML is required for YAML configuration files. "
                            "Install with: pip install PyYAML"
                        )

            self._update_from_dict(config_data)

        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}") from e

    def save_to_file(self, config_file: FilePath, format: str = "json") -> None:
        """
        Save configuration to file.

        Args:
            config_file: Path to save configuration
            format: File format ('json' or 'yaml')

        Raises:
            ConfigurationError: If file cannot be saved
        """
        config_path = Path(config_file)
        config_data = self.to_dict()

        try:
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                if format.lower() == 'json':
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
                elif format.lower() == 'yaml':
                    try:
                        import yaml
                        yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
                    except ImportError:
                        raise ConfigurationError(
                            "PyYAML is required for YAML configuration files. "
                            "Install with: pip install PyYAML"
                        )
                else:
                    raise ConfigurationError(f"Unsupported format: {format}")

        except Exception as e:
            raise ConfigurationError(f"Failed to save configuration: {e}") from e

    def _update_from_dict(self, config_data: Dict[str, Any]) -> None:
        """
        Update configuration from dictionary.

        Args:
            config_data: Configuration dictionary
        """
        if 'processing' in config_data:
            self.processing = ProcessingConfig(**config_data['processing'])
        
        if 'classification' in config_data:
            self.classification = ClassificationConfig(**config_data['classification'])
        
        if 'analysis' in config_data:
            self.analysis = AnalysisConfig(**config_data['analysis'])
        
        if 'visualization' in config_data:
            self.visualization = VisualizationConfig(**config_data['visualization'])

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.

        Returns:
            Configuration as dictionary
        """
        return {
            'processing': self.processing.dict(),
            'classification': self.classification.dict(),
            'analysis': self.analysis.dict(),
            'visualization': self.visualization.dict(),
        }

    def update(self, **kwargs: Any) -> None:
        """
        Update configuration parameters.

        Args:
            **kwargs: Configuration parameters to update
        """
        for section, params in kwargs.items():
            if hasattr(self, section) and isinstance(params, dict):
                config_obj = getattr(self, section)
                for key, value in params.items():
                    if hasattr(config_obj, key):
                        setattr(config_obj, key, value)

    def get_default_config_path(self) -> Path:
        """
        Get default configuration file path.

        Returns:
            Default configuration file path
        """
        # Try user config directory first
        if os.name == 'nt':  # Windows
            config_dir = Path(os.environ.get('APPDATA', '')) / 'microflex'
        else:  # Unix-like
            config_dir = Path.home() / '.config' / 'microflex'
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / 'config.json'

    def create_default_config(self) -> None:
        """Create default configuration file."""
        default_path = self.get_default_config_path()
        if not default_path.exists():
            self.save_to_file(default_path)

    def __repr__(self) -> str:
        """Return string representation of configuration."""
        return f"Config(processing={self.processing}, classification={self.classification}, " \
               f"analysis={self.analysis}, visualization={self.visualization})" 