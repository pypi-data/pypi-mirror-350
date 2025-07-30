"""
Diversity analysis for the microflex library.

This module provides alpha and beta diversity calculations
for microbiome data analysis.
"""

import math
from typing import Dict, List, Optional, Tuple, Union
from collections import Counter

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from scipy.stats import entropy

from microflex.core.base import BaseProcessor
from microflex.core.exceptions import AnalysisError, ValidationError
from microflex.core.types import DiversityMetrics, TaxonomyCollection


class DiversityAnalyzer(BaseProcessor):
    """
    Diversity analyzer for microbiome data.

    This class provides methods to calculate various alpha and beta
    diversity metrics from taxonomic classification results.
    """

    def __init__(self, **kwargs) -> None:
        """Initialize diversity analyzer."""
        super().__init__(**kwargs)

    def calculate_alpha_diversity(
        self,
        abundance_data: Union[Dict[str, int], List[int], pd.Series],
        metrics: Optional[List[str]] = None
    ) -> DiversityMetrics:
        """
        Calculate alpha diversity metrics.

        Args:
            abundance_data: Abundance data (counts or frequencies)
            metrics: List of metrics to calculate (default: all)

        Returns:
            DiversityMetrics object with calculated values
        """
        if metrics is None:
            metrics = ['shannon', 'simpson', 'chao1', 'observed_otus', 'pielou_evenness']

        # Convert input to numpy array
        if isinstance(abundance_data, dict):
            abundances = np.array(list(abundance_data.values()))
        elif isinstance(abundance_data, pd.Series):
            abundances = abundance_data.values
        else:
            abundances = np.array(abundance_data)

        # Remove zero abundances for most calculations
        abundances = abundances[abundances > 0]
        
        if len(abundances) == 0:
            raise ValidationError("No non-zero abundances found")

        results = {}

        # Calculate requested metrics
        if 'shannon' in metrics:
            results['shannon'] = self._calculate_shannon(abundances)

        if 'simpson' in metrics:
            results['simpson'] = self._calculate_simpson(abundances)

        if 'chao1' in metrics:
            results['chao1'] = self._calculate_chao1(abundances)

        if 'observed_otus' in metrics:
            results['observed_otus'] = len(abundances)

        if 'pielou_evenness' in metrics:
            results['pielou_evenness'] = self._calculate_pielou_evenness(abundances)

        if 'fisher_alpha' in metrics:
            results['fisher_alpha'] = self._calculate_fisher_alpha(abundances)

        if 'berger_parker' in metrics:
            results['berger_parker'] = self._calculate_berger_parker(abundances)

        return DiversityMetrics(
            sample_id="sample",
            observed_otus=results.get('observed_otus', 0),
            shannon=results.get('shannon', 0.0),
            simpson=results.get('simpson', 0.0),
            chao1=results.get('chao1'),
            pielou_evenness=results.get('pielou_evenness'),
            metadata={
                'total_abundance': int(np.sum(abundances)),
                'fisher_alpha': results.get('fisher_alpha'),
                'berger_parker_dominance': results.get('berger_parker')
            }
        )

    def _calculate_shannon(self, abundances: np.ndarray) -> float:
        """Calculate Shannon diversity index."""
        proportions = abundances / np.sum(abundances)
        return -np.sum(proportions * np.log(proportions))

    def _calculate_simpson(self, abundances: np.ndarray) -> float:
        """Calculate Simpson diversity index (1 - D)."""
        proportions = abundances / np.sum(abundances)
        return 1 - np.sum(proportions ** 2)

    def _calculate_chao1(self, abundances: np.ndarray) -> float:
        """Calculate Chao1 richness estimator."""
        observed = len(abundances)
        singletons = np.sum(abundances == 1)
        doubletons = np.sum(abundances == 2)
        
        if doubletons > 0:
            chao1 = observed + (singletons ** 2) / (2 * doubletons)
        else:
            chao1 = observed + (singletons * (singletons - 1)) / 2
            
        return float(chao1)

    def _calculate_pielou_evenness(self, abundances: np.ndarray) -> float:
        """Calculate Pielou's evenness index."""
        shannon = self._calculate_shannon(abundances)
        max_shannon = np.log(len(abundances))
        return shannon / max_shannon if max_shannon > 0 else 0.0

    def _calculate_fisher_alpha(self, abundances: np.ndarray) -> float:
        """Calculate Fisher's alpha diversity index."""
        n = np.sum(abundances)
        s = len(abundances)
        
        if n <= s:
            return float('inf')
        
        # Iterative solution for Fisher's alpha
        alpha = 1.0
        for _ in range(100):  # Maximum iterations
            alpha_new = s / np.log(1 + n / alpha)
            if abs(alpha_new - alpha) < 1e-6:
                break
            alpha = alpha_new
            
        return alpha

    def _calculate_berger_parker(self, abundances: np.ndarray) -> float:
        """Calculate Berger-Parker dominance index."""
        return np.max(abundances) / np.sum(abundances)

    def calculate_beta_diversity(
        self,
        abundance_matrix: pd.DataFrame,
        metric: str = 'bray_curtis'
    ) -> pd.DataFrame:
        """
        Calculate beta diversity between samples.

        Args:
            abundance_matrix: DataFrame with samples as rows, taxa as columns
            metric: Distance metric to use

        Returns:
            Distance matrix as DataFrame
        """
        available_metrics = [
            'bray_curtis', 'jaccard', 'euclidean', 'manhattan',
            'cosine', 'correlation', 'hamming'
        ]
        
        if metric not in available_metrics:
            raise ValidationError(f"Metric '{metric}' not supported. Available: {available_metrics}")

        if abundance_matrix.empty:
            raise ValidationError("Abundance matrix is empty")

        # Calculate distance matrix
        if metric == 'bray_curtis':
            distances = self._calculate_bray_curtis(abundance_matrix.values)
        elif metric == 'jaccard':
            distances = self._calculate_jaccard(abundance_matrix.values)
        else:
            # Use scipy for other metrics
            distances = pdist(abundance_matrix.values, metric=metric)
            distances = squareform(distances)

        # Create DataFrame with sample names
        sample_names = abundance_matrix.index
        distance_df = pd.DataFrame(
            distances,
            index=sample_names,
            columns=sample_names
        )

        return distance_df

    def _calculate_bray_curtis(self, matrix: np.ndarray) -> np.ndarray:
        """Calculate Bray-Curtis dissimilarity matrix."""
        n_samples = matrix.shape[0]
        distances = np.zeros((n_samples, n_samples))
        
        for i in range(n_samples):
            for j in range(i + 1, n_samples):
                numerator = np.sum(np.abs(matrix[i] - matrix[j]))
                denominator = np.sum(matrix[i] + matrix[j])
                
                if denominator > 0:
                    distance = numerator / denominator
                else:
                    distance = 0.0
                    
                distances[i, j] = distance
                distances[j, i] = distance
                
        return distances

    def _calculate_jaccard(self, matrix: np.ndarray) -> np.ndarray:
        """Calculate Jaccard dissimilarity matrix."""
        # Convert to presence/absence
        binary_matrix = (matrix > 0).astype(int)
        n_samples = binary_matrix.shape[0]
        distances = np.zeros((n_samples, n_samples))
        
        for i in range(n_samples):
            for j in range(i + 1, n_samples):
                intersection = np.sum(binary_matrix[i] & binary_matrix[j])
                union = np.sum(binary_matrix[i] | binary_matrix[j])
                
                if union > 0:
                    jaccard_similarity = intersection / union
                    distance = 1 - jaccard_similarity
                else:
                    distance = 0.0
                    
                distances[i, j] = distance
                distances[j, i] = distance
                
        return distances

    def create_abundance_matrix_from_taxonomy(
        self,
        taxonomy_results: List[TaxonomyCollection],
        sample_names: Optional[List[str]] = None,
        taxonomic_level: str = 'genus'
    ) -> pd.DataFrame:
        """
        Create abundance matrix from taxonomy results.

        Args:
            taxonomy_results: List of taxonomy collections (one per sample)
            sample_names: Names for samples
            taxonomic_level: Taxonomic level to aggregate at

        Returns:
            Abundance matrix DataFrame
        """
        if not taxonomy_results:
            raise ValidationError("No taxonomy results provided")

        if sample_names is None:
            sample_names = [f"Sample_{i+1}" for i in range(len(taxonomy_results))]

        if len(sample_names) != len(taxonomy_results):
            raise ValidationError("Number of sample names must match number of taxonomy results")

        # Collect all taxa across samples
        all_taxa = set()
        sample_counts = []

        for sample_results in taxonomy_results:
            taxa_counts = Counter()
            
            for result in sample_results:
                taxon = getattr(result, taxonomic_level)
                if taxon is not None:
                    taxa_counts[taxon] += 1
                    all_taxa.add(taxon)
            
            sample_counts.append(taxa_counts)

        # Create abundance matrix
        all_taxa = sorted(list(all_taxa))
        abundance_matrix = []

        for taxa_counts in sample_counts:
            row = [taxa_counts.get(taxon, 0) for taxon in all_taxa]
            abundance_matrix.append(row)

        return pd.DataFrame(
            abundance_matrix,
            index=sample_names,
            columns=all_taxa
        )

    def calculate_rarefaction_curve(
        self,
        abundance_data: Union[Dict[str, int], List[int], pd.Series],
        max_depth: Optional[int] = None,
        step_size: int = 100,
        iterations: int = 10
    ) -> Tuple[List[int], List[float], List[float]]:
        """
        Calculate rarefaction curve.

        Args:
            abundance_data: Abundance data
            max_depth: Maximum rarefaction depth
            step_size: Step size for rarefaction
            iterations: Number of iterations for averaging

        Returns:
            Tuple of (depths, mean_richness, std_richness)
        """
        # Convert to list of individuals
        if isinstance(abundance_data, dict):
            individuals = []
            for taxon, count in abundance_data.items():
                individuals.extend([taxon] * count)
        elif isinstance(abundance_data, pd.Series):
            individuals = []
            for taxon, count in abundance_data.items():
                individuals.extend([taxon] * int(count))
        else:
            # Assume it's already a list of abundances
            individuals = []
            for i, count in enumerate(abundance_data):
                individuals.extend([f"OTU_{i}"] * int(count))

        total_individuals = len(individuals)
        
        if max_depth is None:
            max_depth = total_individuals

        max_depth = min(max_depth, total_individuals)
        depths = list(range(step_size, max_depth + 1, step_size))
        
        if max_depth not in depths:
            depths.append(max_depth)

        richness_values = []
        
        for depth in depths:
            iteration_richness = []
            
            for _ in range(iterations):
                # Random subsample
                subsample = np.random.choice(individuals, size=depth, replace=False)
                richness = len(set(subsample))
                iteration_richness.append(richness)
            
            richness_values.append(iteration_richness)

        # Calculate means and standard deviations
        mean_richness = [np.mean(values) for values in richness_values]
        std_richness = [np.std(values) for values in richness_values]

        return depths, mean_richness, std_richness

    def _process_implementation(self, data) -> Dict:
        """
        Process implementation for BaseProcessor interface.

        Args:
            data: Input data

        Returns:
            Processing results
        """
        # This is a placeholder - specific analysis methods should be called directly
        return {"message": "Use specific diversity calculation methods"}


class AlphaDiversityCalculator(DiversityAnalyzer):
    """Specialized calculator for alpha diversity metrics."""

    def __init__(self, metrics: Optional[List[str]] = None, **kwargs) -> None:
        """
        Initialize alpha diversity calculator.

        Args:
            metrics: List of metrics to calculate by default
            **kwargs: Additional configuration parameters
        """
        super().__init__(**kwargs)
        self.default_metrics = metrics or ['shannon', 'simpson', 'chao1', 'observed_otus']

    def _process_implementation(self, data: Union[Dict, List, pd.Series]) -> DiversityMetrics:
        """Calculate alpha diversity for input data."""
        return self.calculate_alpha_diversity(data, self.default_metrics)


class BetaDiversityCalculator(DiversityAnalyzer):
    """Specialized calculator for beta diversity metrics."""

    def __init__(self, metric: str = 'bray_curtis', **kwargs) -> None:
        """
        Initialize beta diversity calculator.

        Args:
            metric: Default distance metric to use
            **kwargs: Additional configuration parameters
        """
        super().__init__(**kwargs)
        self.default_metric = metric

    def _process_implementation(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate beta diversity for input abundance matrix."""
        return self.calculate_beta_diversity(data, self.default_metric) 