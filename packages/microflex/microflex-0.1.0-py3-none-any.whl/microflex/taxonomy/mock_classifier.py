"""
Mock taxonomic classifier for the microflex library.

This module provides a mock classifier for testing and demonstration
purposes that doesn't require external tools.
"""

import random
from typing import Dict, List, Optional

from microflex.core.base import BaseProcessor
from microflex.core.types import (
    SequenceData,
    SequenceCollection,
    TaxonomyResult,
    TaxonomyCollection,
)


class MockClassifier(BaseProcessor):
    """
    Mock taxonomic classifier for testing and demonstration.

    This classifier generates realistic-looking taxonomic classifications
    without requiring external databases or tools.
    """

    def __init__(
        self,
        confidence_range: tuple = (70.0, 95.0),
        classification_rate: float = 0.8,
        **kwargs
    ) -> None:
        """
        Initialize mock classifier.

        Args:
            confidence_range: Range of confidence scores to generate
            classification_rate: Fraction of sequences that get classified
            **kwargs: Additional configuration parameters
        """
        super().__init__(
            confidence_range=confidence_range,
            classification_rate=classification_rate,
            **kwargs
        )

        # Mock taxonomy database
        self.mock_taxa = [
            {
                'kingdom': 'Bacteria',
                'phylum': 'Proteobacteria',
                'class': 'Gammaproteobacteria',
                'order': 'Enterobacterales',
                'family': 'Enterobacteriaceae',
                'genus': 'Escherichia',
                'species': 'Escherichia coli'
            },
            {
                'kingdom': 'Bacteria',
                'phylum': 'Firmicutes',
                'class': 'Bacilli',
                'order': 'Lactobacillales',
                'family': 'Lactobacillaceae',
                'genus': 'Lactobacillus',
                'species': 'Lactobacillus acidophilus'
            },
            {
                'kingdom': 'Bacteria',
                'phylum': 'Bacteroidetes',
                'class': 'Bacteroidia',
                'order': 'Bacteroidales',
                'family': 'Bacteroidaceae',
                'genus': 'Bacteroides',
                'species': 'Bacteroides fragilis'
            },
            {
                'kingdom': 'Bacteria',
                'phylum': 'Actinobacteria',
                'class': 'Actinobacteria',
                'order': 'Bifidobacteriales',
                'family': 'Bifidobacteriaceae',
                'genus': 'Bifidobacterium',
                'species': 'Bifidobacterium longum'
            },
            {
                'kingdom': 'Bacteria',
                'phylum': 'Proteobacteria',
                'class': 'Alphaproteobacteria',
                'order': 'Rhizobiales',
                'family': 'Rhizobiaceae',
                'genus': 'Rhizobium',
                'species': 'Rhizobium leguminosarum'
            },
            {
                'kingdom': 'Bacteria',
                'phylum': 'Firmicutes',
                'class': 'Clostridia',
                'order': 'Clostridiales',
                'family': 'Clostridiaceae',
                'genus': 'Clostridium',
                'species': 'Clostridium difficile'
            },
            {
                'kingdom': 'Bacteria',
                'phylum': 'Cyanobacteria',
                'class': 'Cyanophyceae',
                'order': 'Nostocales',
                'family': 'Nostocaceae',
                'genus': 'Nostoc',
                'species': 'Nostoc commune'
            },
            {
                'kingdom': 'Archaea',
                'phylum': 'Euryarchaeota',
                'class': 'Methanobacteria',
                'order': 'Methanobacteriales',
                'family': 'Methanobacteriaceae',
                'genus': 'Methanobrevibacter',
                'species': 'Methanobrevibacter smithii'
            },
            {
                'kingdom': 'Bacteria',
                'phylum': 'Proteobacteria',
                'class': 'Betaproteobacteria',
                'order': 'Burkholderiales',
                'family': 'Burkholderiaceae',
                'genus': 'Burkholderia',
                'species': 'Burkholderia cepacia'
            },
            {
                'kingdom': 'Bacteria',
                'phylum': 'Spirochaetes',
                'class': 'Spirochaetia',
                'order': 'Spirochaetales',
                'family': 'Spirochaetaceae',
                'genus': 'Treponema',
                'species': 'Treponema pallidum'
            }
        ]

    def _process_implementation(self, data: SequenceCollection) -> TaxonomyCollection:
        """
        Generate mock taxonomic classifications.

        Args:
            data: Input sequence collection

        Returns:
            Collection of taxonomy results
        """
        taxonomy_results = []
        
        confidence_range = self.get_config_parameter('confidence_range')
        classification_rate = self.get_config_parameter('classification_rate')

        for seq_data in data:
            # Determine if this sequence gets classified
            if random.random() < classification_rate:
                # Select random taxon
                taxon = random.choice(self.mock_taxa)
                
                # Generate confidence score
                confidence = random.uniform(confidence_range[0], confidence_range[1])
                
                # Determine classification depth based on confidence
                classification_depth = self._determine_classification_depth(confidence)
                
                # Create taxonomy result
                tax_result = TaxonomyResult(
                    sequence_id=seq_data.sequence_id,
                    kingdom=taxon['kingdom'] if classification_depth >= 1 else None,
                    phylum=taxon['phylum'] if classification_depth >= 2 else None,
                    class_=taxon['class'] if classification_depth >= 3 else None,
                    order=taxon['order'] if classification_depth >= 4 else None,
                    family=taxon['family'] if classification_depth >= 5 else None,
                    genus=taxon['genus'] if classification_depth >= 6 else None,
                    species=taxon['species'] if classification_depth >= 7 else None,
                    confidence=confidence,
                    method="mock_classifier",
                    database="mock_database",
                    metadata={
                        'classification_depth': classification_depth,
                        'sequence_length': seq_data.length,
                        'mock_hit_id': f"mock_{random.randint(1000, 9999)}"
                    }
                )
            else:
                # No classification
                tax_result = TaxonomyResult(
                    sequence_id=seq_data.sequence_id,
                    kingdom=None,
                    phylum=None,
                    class_=None,
                    order=None,
                    family=None,
                    genus=None,
                    species=None,
                    confidence=0.0,
                    method="mock_classifier",
                    database="mock_database",
                    metadata={'status': 'unclassified'}
                )

            taxonomy_results.append(tax_result)

        return taxonomy_results

    def _determine_classification_depth(self, confidence: float) -> int:
        """
        Determine classification depth based on confidence score.

        Args:
            confidence: Confidence score

        Returns:
            Classification depth (1-7, corresponding to kingdom-species)
        """
        if confidence >= 95:
            return 7  # Species level
        elif confidence >= 90:
            return 6  # Genus level
        elif confidence >= 85:
            return 5  # Family level
        elif confidence >= 80:
            return 4  # Order level
        elif confidence >= 75:
            return 3  # Class level
        elif confidence >= 70:
            return 2  # Phylum level
        else:
            return 1  # Kingdom level

    def add_custom_taxon(self, taxon: Dict[str, str]) -> None:
        """
        Add a custom taxon to the mock database.

        Args:
            taxon: Dictionary with taxonomic levels
        """
        required_keys = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
        if all(key in taxon for key in required_keys):
            self.mock_taxa.append(taxon)
        else:
            raise ValueError(f"Taxon must contain all required keys: {required_keys}")

    def get_mock_database_stats(self) -> Dict[str, int]:
        """
        Get statistics about the mock database.

        Returns:
            Dictionary with database statistics
        """
        kingdoms = set()
        phyla = set()
        classes = set()
        orders = set()
        families = set()
        genera = set()
        species = set()

        for taxon in self.mock_taxa:
            kingdoms.add(taxon['kingdom'])
            phyla.add(taxon['phylum'])
            classes.add(taxon['class'])
            orders.add(taxon['order'])
            families.add(taxon['family'])
            genera.add(taxon['genus'])
            species.add(taxon['species'])

        return {
            'total_taxa': len(self.mock_taxa),
            'kingdoms': len(kingdoms),
            'phyla': len(phyla),
            'classes': len(classes),
            'orders': len(orders),
            'families': len(families),
            'genera': len(genera),
            'species': len(species)
        }

    def classify_single_sequence(self, sequence: SequenceData) -> TaxonomyResult:
        """
        Classify a single sequence.

        Args:
            sequence: Sequence to classify

        Returns:
            Taxonomy result
        """
        results = self.process([sequence])
        return results[0] if results else TaxonomyResult(
            sequence_id=sequence.sequence_id,
            method="mock_classifier",
            database="mock_database",
            metadata={'status': 'classification_failed'}
        ) 