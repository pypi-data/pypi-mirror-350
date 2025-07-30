"""
BLAST-based taxonomic classifier for the microflex library.

This module provides taxonomic classification using BLAST+ tools
against various reference databases.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, List, Any
import xml.etree.ElementTree as ET

import pandas as pd

from microflex.core.base import BaseProcessor
from microflex.core.exceptions import ClassificationError, DependencyError, ValidationError
from microflex.core.types import (
    SequenceData,
    SequenceCollection,
    TaxonomyResult,
    TaxonomyCollection,
    FilePath,
)


class BlastClassifier(BaseProcessor):
    """
    BLAST-based taxonomic classifier.

    This classifier uses BLAST+ tools to perform taxonomic classification
    against reference databases like NCBI NT/NR or custom databases.
    """

    def __init__(
        self,
        database_path: FilePath,
        blast_program: str = "blastn",
        evalue: float = 1e-5,
        max_target_seqs: int = 10,
        word_size: Optional[int] = None,
        perc_identity: float = 80.0,
        qcov_hsp_perc: float = 50.0,
        **kwargs
    ) -> None:
        """
        Initialize BLAST classifier.

        Args:
            database_path: Path to BLAST database
            blast_program: BLAST program to use (blastn, blastp, blastx, etc.)
            evalue: E-value threshold
            max_target_seqs: Maximum number of target sequences
            word_size: Word size for BLAST search
            perc_identity: Minimum percent identity
            qcov_hsp_perc: Minimum query coverage per HSP
            **kwargs: Additional configuration parameters
        """
        super().__init__(
            database_path=str(database_path),
            blast_program=blast_program,
            evalue=evalue,
            max_target_seqs=max_target_seqs,
            word_size=word_size,
            perc_identity=perc_identity,
            qcov_hsp_perc=qcov_hsp_perc,
            **kwargs
        )

        self.database_path = Path(database_path)
        self.blast_program = blast_program

        # Validate BLAST program
        valid_programs = ["blastn", "blastp", "blastx", "tblastn", "tblastx"]
        if blast_program not in valid_programs:
            raise ValidationError(f"Invalid BLAST program: {blast_program}")

        # Check if BLAST+ is available
        self._check_blast_availability()

        # Validate database
        self._validate_database()

    def _check_blast_availability(self) -> None:
        """Check if BLAST+ tools are available."""
        try:
            result = subprocess.run(
                [self.blast_program, "-version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                raise DependencyError(f"BLAST+ program {self.blast_program} not found")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            raise DependencyError(
                f"BLAST+ tools not found. Please install BLAST+ and ensure "
                f"{self.blast_program} is in your PATH"
            )

    def _validate_database(self) -> None:
        """Validate BLAST database exists."""
        # Check for database files (at least .nhr, .nin, .nsq for nucleotide)
        db_extensions = [".nhr", ".nin", ".nsq"] if "n" in self.blast_program else [".phr", ".pin", ".psq"]
        
        for ext in db_extensions:
            db_file = Path(str(self.database_path) + ext)
            if not db_file.exists():
                raise ValidationError(f"BLAST database file not found: {db_file}")

    def _process_implementation(self, data: SequenceCollection) -> TaxonomyCollection:
        """
        Classify sequences using BLAST.

        Args:
            data: Input sequence collection

        Returns:
            Collection of taxonomy results
        """
        if not data:
            return []

        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as query_file:
            query_path = Path(query_file.name)
            
            # Write sequences to temporary FASTA file
            self._write_sequences_to_fasta(data, query_file)

        try:
            # Run BLAST
            blast_results = self._run_blast(query_path)
            
            # Parse results
            taxonomy_results = self._parse_blast_results(blast_results, data)
            
            return taxonomy_results

        finally:
            # Clean up temporary files
            if query_path.exists():
                query_path.unlink()

    def _write_sequences_to_fasta(self, sequences: SequenceCollection, file_handle) -> None:
        """Write sequences to FASTA file."""
        for seq_data in sequences:
            file_handle.write(f">{seq_data.sequence_id}\n")
            file_handle.write(f"{seq_data.sequence}\n")

    def _run_blast(self, query_path: Path) -> Path:
        """
        Run BLAST search.

        Args:
            query_path: Path to query FASTA file

        Returns:
            Path to BLAST output file
        """
        # Create output file
        output_path = query_path.with_suffix('.xml')

        # Build BLAST command
        cmd = [
            self.blast_program,
            "-query", str(query_path),
            "-db", str(self.database_path),
            "-out", str(output_path),
            "-outfmt", "5",  # XML format
            "-evalue", str(self.get_config_parameter('evalue')),
            "-max_target_seqs", str(self.get_config_parameter('max_target_seqs')),
        ]

        # Add optional parameters
        word_size = self.get_config_parameter('word_size')
        if word_size is not None:
            cmd.extend(["-word_size", str(word_size)])

        perc_identity = self.get_config_parameter('perc_identity')
        if perc_identity is not None:
            cmd.extend(["-perc_identity", str(perc_identity)])

        qcov_hsp_perc = self.get_config_parameter('qcov_hsp_perc')
        if qcov_hsp_perc is not None:
            cmd.extend(["-qcov_hsp_perc", str(qcov_hsp_perc)])

        try:
            # Run BLAST
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode != 0:
                raise ClassificationError(f"BLAST failed: {result.stderr}")

            return output_path

        except subprocess.TimeoutExpired:
            raise ClassificationError("BLAST search timed out")
        except Exception as e:
            raise ClassificationError(f"BLAST execution failed: {e}")

    def _parse_blast_results(self, blast_output_path: Path, original_sequences: SequenceCollection) -> TaxonomyCollection:
        """
        Parse BLAST XML output.

        Args:
            blast_output_path: Path to BLAST XML output
            original_sequences: Original sequence data

        Returns:
            Collection of taxonomy results
        """
        taxonomy_results = []

        try:
            # Parse XML
            tree = ET.parse(blast_output_path)
            root = tree.getroot()

            # Create sequence ID to sequence data mapping
            seq_map = {seq.sequence_id: seq for seq in original_sequences}

            # Parse iterations (queries)
            for iteration in root.findall('.//Iteration'):
                query_id = iteration.find('Iteration_query-def').text
                
                # Get original sequence data
                original_seq = seq_map.get(query_id)
                
                # Parse hits
                hits = iteration.findall('.//Hit')
                
                if hits:
                    # Take best hit
                    best_hit = hits[0]
                    
                    # Extract hit information
                    hit_def = best_hit.find('Hit_def').text
                    hit_accession = best_hit.find('Hit_accession').text
                    
                    # Get HSP information
                    hsp = best_hit.find('.//Hsp')
                    if hsp is not None:
                        evalue = float(hsp.find('Hsp_evalue').text)
                        bit_score = float(hsp.find('Hsp_bit-score').text)
                        identity = int(hsp.find('Hsp_identity').text)
                        align_len = int(hsp.find('Hsp_align-len').text)
                        
                        # Calculate percent identity
                        percent_identity = (identity / align_len) * 100
                        
                        # Parse taxonomy from hit definition
                        taxonomy_info = self._parse_taxonomy_from_hit(hit_def)
                        
                        # Create taxonomy result
                        tax_result = TaxonomyResult(
                            sequence_id=query_id,
                            kingdom=taxonomy_info.get('kingdom'),
                            phylum=taxonomy_info.get('phylum'),
                            class_=taxonomy_info.get('class'),
                            order=taxonomy_info.get('order'),
                            family=taxonomy_info.get('family'),
                            genus=taxonomy_info.get('genus'),
                            species=taxonomy_info.get('species'),
                            confidence=percent_identity,
                            method="blast",
                            database=str(self.database_path),
                            metadata={
                                'hit_accession': hit_accession,
                                'hit_definition': hit_def,
                                'evalue': evalue,
                                'bit_score': bit_score,
                                'percent_identity': percent_identity,
                                'alignment_length': align_len,
                                'blast_program': self.blast_program
                            }
                        )
                        
                        taxonomy_results.append(tax_result)
                else:
                    # No hits found
                    tax_result = TaxonomyResult(
                        sequence_id=query_id,
                        kingdom=None,
                        phylum=None,
                        class_=None,
                        order=None,
                        family=None,
                        genus=None,
                        species=None,
                        confidence=0.0,
                        method="blast",
                        database=str(self.database_path),
                        metadata={'status': 'no_hits'}
                    )
                    
                    taxonomy_results.append(tax_result)

        except ET.ParseError as e:
            raise ClassificationError(f"Failed to parse BLAST XML output: {e}")
        except Exception as e:
            raise ClassificationError(f"Error parsing BLAST results: {e}")
        finally:
            # Clean up output file
            if blast_output_path.exists():
                blast_output_path.unlink()

        return taxonomy_results

    def _parse_taxonomy_from_hit(self, hit_definition: str) -> Dict[str, Optional[str]]:
        """
        Parse taxonomic information from BLAST hit definition.

        Args:
            hit_definition: BLAST hit definition line

        Returns:
            Dictionary with taxonomic levels
        """
        # This is a simplified parser - in practice, you'd want to use
        # NCBI taxonomy database or other structured taxonomy sources
        
        taxonomy = {
            'kingdom': None,
            'phylum': None,
            'class': None,
            'order': None,
            'family': None,
            'genus': None,
            'species': None
        }

        # Simple parsing based on common patterns
        hit_lower = hit_definition.lower()
        
        # Extract genus and species from binomial nomenclature
        words = hit_definition.split()
        if len(words) >= 2:
            # Look for genus species pattern
            for i in range(len(words) - 1):
                word1, word2 = words[i], words[i + 1]
                if (word1[0].isupper() and word1[1:].islower() and 
                    word2.islower() and len(word1) > 2 and len(word2) > 2):
                    taxonomy['genus'] = word1
                    taxonomy['species'] = f"{word1} {word2}"
                    break

        # Simple kingdom detection
        if any(term in hit_lower for term in ['bacteria', 'bacterial']):
            taxonomy['kingdom'] = 'Bacteria'
        elif any(term in hit_lower for term in ['archaea', 'archaeal']):
            taxonomy['kingdom'] = 'Archaea'
        elif any(term in hit_lower for term in ['eukaryot', 'fungal', 'plant']):
            taxonomy['kingdom'] = 'Eukaryota'

        return taxonomy

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
            method="blast",
            database=str(self.database_path),
            metadata={'status': 'classification_failed'}
        )

    def get_database_info(self) -> Dict[str, Any]:
        """
        Get information about the BLAST database.

        Returns:
            Dictionary with database information
        """
        try:
            result = subprocess.run(
                ["blastdbcmd", "-db", str(self.database_path), "-info"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return {
                    'database_path': str(self.database_path),
                    'info': result.stdout,
                    'available': True
                }
            else:
                return {
                    'database_path': str(self.database_path),
                    'error': result.stderr,
                    'available': False
                }
        except Exception as e:
            return {
                'database_path': str(self.database_path),
                'error': str(e),
                'available': False
            } 