#!/usr/bin/env python3
"""
Main CLI entry point for microflex.

This module provides the command-line interface for microflex
with subcommands for different analysis tasks.
"""

import sys
from pathlib import Path
from typing import Optional

import click
import pandas as pd

from microflex import __version__
from microflex.core.types import SequenceData
from microflex.io import FastqReader, FastaReader, SequenceWriter
from microflex.preprocess import QualityFilter
from microflex.taxonomy import MockClassifier
from microflex.analysis import DiversityAnalyzer


@click.group()
@click.version_option(version=__version__)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    """
    Microflex: Cross-platform Python toolkit for microbiome analysis.
    
    Supports multiple sequencing technologies including Illumina NGS,
    Oxford Nanopore, and Sanger sequencing.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--min-length', type=int, default=100, help='Minimum sequence length')
@click.option('--min-quality', type=float, default=20.0, help='Minimum average quality score')
@click.option('--max-n-content', type=float, default=0.1, help='Maximum N content (0-1)')
@click.pass_context
def filter(ctx, input_file, output, min_length, min_quality, max_n_content):
    """Filter sequences based on quality criteria."""
    verbose = ctx.obj['verbose']
    
    if verbose:
        click.echo(f"🔍 Filtering sequences from {input_file}")
        click.echo(f"   Min length: {min_length}")
        click.echo(f"   Min quality: {min_quality}")
        click.echo(f"   Max N content: {max_n_content}")
    
    # Determine input format and read sequences
    input_path = Path(input_file)
    if input_path.suffix.lower() in ['.fastq', '.fq']:
        reader = FastqReader()
    elif input_path.suffix.lower() in ['.fasta', '.fa']:
        reader = FastaReader()
    else:
        click.echo(f"❌ Unsupported file format: {input_path.suffix}", err=True)
        sys.exit(1)
    
    try:
        sequences = reader.read(input_path)
        if verbose:
            click.echo(f"   Read {len(sequences)} sequences")
        
        # Apply quality filter
        quality_filter = QualityFilter(
            min_length=min_length,
            min_quality_score=min_quality,
            max_n_content=max_n_content
        )
        
        filtered_sequences = quality_filter.process(sequences)
        
        if verbose:
            click.echo(f"   Filtered to {len(filtered_sequences)} sequences")
            click.echo(f"   Filter rate: {(1 - len(filtered_sequences)/len(sequences))*100:.1f}%")
        
        # Write output
        if output is None:
            output = input_path.with_suffix('.filtered' + input_path.suffix)
        
        writer = SequenceWriter()
        writer.write(filtered_sequences, output)
        
        click.echo(f"✅ Filtered sequences saved to {output}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--method', type=click.Choice(['mock']), default='mock', help='Classification method')
@click.option('--confidence-threshold', type=float, default=70.0, help='Minimum confidence threshold')
@click.pass_context
def classify(ctx, input_file, output, method, confidence_threshold):
    """Perform taxonomic classification of sequences."""
    verbose = ctx.obj['verbose']
    
    if verbose:
        click.echo(f"🔬 Classifying sequences from {input_file}")
        click.echo(f"   Method: {method}")
        click.echo(f"   Confidence threshold: {confidence_threshold}")
    
    # Read sequences
    input_path = Path(input_file)
    if input_path.suffix.lower() in ['.fastq', '.fq']:
        reader = FastqReader()
    elif input_path.suffix.lower() in ['.fasta', '.fa']:
        reader = FastaReader()
    else:
        click.echo(f"❌ Unsupported file format: {input_path.suffix}", err=True)
        sys.exit(1)
    
    try:
        sequences = reader.read(input_path)
        if verbose:
            click.echo(f"   Read {len(sequences)} sequences")
        
        # Perform classification
        if method == 'mock':
            classifier = MockClassifier(
                confidence_range=(confidence_threshold, 95.0),
                classification_rate=0.8
            )
        else:
            click.echo(f"❌ Unsupported classification method: {method}", err=True)
            sys.exit(1)
        
        taxonomy_results = classifier.process(sequences)
        
        # Count classifications
        classified = sum(1 for r in taxonomy_results if r.genus is not None)
        if verbose:
            click.echo(f"   Classified {classified}/{len(taxonomy_results)} sequences ({classified/len(taxonomy_results)*100:.1f}%)")
        
        # Save results
        if output is None:
            output = input_path.with_suffix('.taxonomy.tsv')
        
        # Convert to DataFrame and save
        results_data = []
        for result in taxonomy_results:
            results_data.append({
                'sequence_id': result.sequence_id,
                'kingdom': result.kingdom,
                'phylum': result.phylum,
                'class': result.class_,
                'order': result.order,
                'family': result.family,
                'genus': result.genus,
                'species': result.species,
                'confidence': result.confidence,
                'method': result.method
            })
        
        df = pd.DataFrame(results_data)
        df.to_csv(output, sep='\t', index=False)
        
        click.echo(f"✅ Taxonomy results saved to {output}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('taxonomy_file', type=click.Path(exists=True))
@click.option('--output-dir', '-o', type=click.Path(), help='Output directory')
@click.option('--level', type=click.Choice(['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']), 
              default='genus', help='Taxonomic level for analysis')
@click.option('--sample-column', default='sample', help='Column name for sample grouping')
@click.pass_context
def analyze(ctx, taxonomy_file, output_dir, level, sample_column):
    """Perform diversity analysis on taxonomy results."""
    verbose = ctx.obj['verbose']
    
    if verbose:
        click.echo(f"📊 Analyzing diversity from {taxonomy_file}")
        click.echo(f"   Taxonomic level: {level}")
        click.echo(f"   Sample column: {sample_column}")
    
    try:
        # Read taxonomy results
        df = pd.read_csv(taxonomy_file, sep='\t')
        
        if verbose:
            click.echo(f"   Read {len(df)} taxonomy results")
        
        # Group by sample if sample column exists
        if sample_column in df.columns:
            samples = df[sample_column].unique()
            if verbose:
                click.echo(f"   Found {len(samples)} samples")
        else:
            # Treat all as one sample
            df[sample_column] = 'Sample_1'
            samples = ['Sample_1']
            if verbose:
                click.echo("   No sample column found, treating as single sample")
        
        # Create abundance matrix
        abundance_data = []
        for sample in samples:
            sample_df = df[df[sample_column] == sample]
            taxa_counts = sample_df[level].value_counts().to_dict()
            abundance_data.append(taxa_counts)
        
        # Convert to abundance matrix
        all_taxa = set()
        for counts in abundance_data:
            all_taxa.update(counts.keys())
        all_taxa = sorted([t for t in all_taxa if pd.notna(t)])
        
        abundance_matrix = []
        for counts in abundance_data:
            row = [counts.get(taxon, 0) for taxon in all_taxa]
            abundance_matrix.append(row)
        
        abundance_df = pd.DataFrame(abundance_matrix, index=samples, columns=all_taxa)
        
        if verbose:
            click.echo(f"   Created abundance matrix: {abundance_df.shape}")
        
        # Calculate diversity metrics
        analyzer = DiversityAnalyzer()
        
        # Alpha diversity
        alpha_results = {}
        for sample in samples:
            sample_abundances = abundance_df.loc[sample]
            sample_abundances = sample_abundances[sample_abundances > 0]
            
            if len(sample_abundances) > 0:
                metrics = analyzer.calculate_alpha_diversity(sample_abundances)
                alpha_results[sample] = metrics
        
        # Beta diversity
        beta_distances = analyzer.calculate_beta_diversity(abundance_df)
        
        # Save results
        if output_dir is None:
            output_dir = Path(taxonomy_file).parent / 'analysis_results'
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        # Save abundance matrix
        abundance_df.to_csv(output_dir / 'abundance_matrix.csv')
        
        # Save alpha diversity
        alpha_df = pd.DataFrame({
            sample: {
                'shannon': metrics.shannon,
                'simpson': metrics.simpson,
                'chao1': metrics.chao1,
                'observed': metrics.observed_otus,
                'evenness': metrics.pielou_evenness
            }
            for sample, metrics in alpha_results.items()
        }).T
        alpha_df.to_csv(output_dir / 'alpha_diversity.csv')
        
        # Save beta diversity
        beta_distances.to_csv(output_dir / 'beta_diversity.csv')
        
        if verbose:
            click.echo(f"   Alpha diversity calculated for {len(alpha_results)} samples")
            click.echo(f"   Beta diversity matrix: {beta_distances.shape}")
        
        click.echo(f"✅ Analysis results saved to {output_dir}")
        
        # Print summary
        if alpha_results:
            avg_shannon = sum(m.shannon for m in alpha_results.values()) / len(alpha_results)
            avg_simpson = sum(m.simpson for m in alpha_results.values()) / len(alpha_results)
            avg_richness = sum(m.observed_otus for m in alpha_results.values()) / len(alpha_results)
            
            click.echo("\n📈 Summary Statistics:")
            click.echo(f"   Average Shannon diversity: {avg_shannon:.2f}")
            click.echo(f"   Average Simpson diversity: {avg_simpson:.2f}")
            click.echo(f"   Average observed richness: {avg_richness:.1f}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', type=click.Choice(['fasta', 'fastq']), help='Output format')
@click.pass_context
def convert(ctx, input_file, output, format):
    """Convert between sequence file formats."""
    verbose = ctx.obj['verbose']
    
    if verbose:
        click.echo(f"🔄 Converting {input_file}")
    
    # Determine input format
    input_path = Path(input_file)
    if input_path.suffix.lower() in ['.fastq', '.fq']:
        reader = FastqReader()
        input_format = 'fastq'
    elif input_path.suffix.lower() in ['.fasta', '.fa']:
        reader = FastaReader()
        input_format = 'fasta'
    else:
        click.echo(f"❌ Unsupported input format: {input_path.suffix}", err=True)
        sys.exit(1)
    
    # Determine output format
    if format is None:
        if input_format == 'fastq':
            format = 'fasta'
        else:
            format = 'fastq'
    
    if output is None:
        if format == 'fasta':
            output = input_path.with_suffix('.fasta')
        else:
            output = input_path.with_suffix('.fastq')
    
    try:
        sequences = reader.read(input_path)
        if verbose:
            click.echo(f"   Read {len(sequences)} sequences")
            click.echo(f"   Converting from {input_format} to {format}")
        
        writer = SequenceWriter()
        writer.write(sequences, output, file_format=format)
        
        click.echo(f"✅ Converted sequences saved to {output}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.pass_context
def info(ctx, input_file):
    """Display information about a sequence file."""
    verbose = ctx.obj['verbose']
    
    click.echo(f"📋 File Information: {input_file}")
    
    # Determine format and read
    input_path = Path(input_file)
    if input_path.suffix.lower() in ['.fastq', '.fq']:
        reader = FastqReader()
        file_format = 'FASTQ'
    elif input_path.suffix.lower() in ['.fasta', '.fa']:
        reader = FastaReader()
        file_format = 'FASTA'
    else:
        click.echo(f"❌ Unsupported file format: {input_path.suffix}", err=True)
        sys.exit(1)
    
    try:
        sequences = reader.read(input_path)
        
        # Calculate statistics
        total_sequences = len(sequences)
        total_bases = sum(len(seq.sequence) for seq in sequences)
        lengths = [len(seq.sequence) for seq in sequences]
        
        min_length = min(lengths) if lengths else 0
        max_length = max(lengths) if lengths else 0
        avg_length = total_bases / total_sequences if total_sequences > 0 else 0
        
        # Quality statistics (if available)
        has_quality = any(seq.quality is not None for seq in sequences)
        
        click.echo(f"   Format: {file_format}")
        click.echo(f"   Total sequences: {total_sequences:,}")
        click.echo(f"   Total bases: {total_bases:,}")
        click.echo(f"   Average length: {avg_length:.1f}")
        click.echo(f"   Length range: {min_length} - {max_length}")
        click.echo(f"   Has quality scores: {'Yes' if has_quality else 'No'}")
        
        if has_quality and verbose:
            quality_scores = []
            for seq in sequences:
                if seq.quality:
                    quality_scores.extend(seq.quality.scores)
            
            if quality_scores:
                avg_quality = sum(quality_scores) / len(quality_scores)
                min_quality = min(quality_scores)
                max_quality = max(quality_scores)
                
                click.echo(f"   Average quality: {avg_quality:.1f}")
                click.echo(f"   Quality range: {min_quality} - {max_quality}")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main() 