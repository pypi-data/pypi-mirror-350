"""
microflex: Cross-platform Python toolkit for microbiome analysis.

A comprehensive toolkit for analyzing microbiome data from multiple sequencing
technologies including Illumina (NGS), Oxford Nanopore, and Sanger sequencing.
"""

__version__ = "0.1.0"
__author__ = "Ata Umut Özsoy"
__email__ = "ata.ozsoy@example.com"
__license__ = "MIT"

# Core imports for easy access
from microflex.core.exceptions import MicroflexError
from microflex.core.types import SequenceData, TaxonomyResult

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "MicroflexError",
    "SequenceData",
    "TaxonomyResult",
] 