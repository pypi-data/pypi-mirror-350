# microflex

[![PyPI version](https://badge.fury.io/py/microflex.svg)](https://badge.fury.io/py/microflex)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A cross-platform Python toolkit for microbiome analysis using multiple sequencing technologies including Illumina (NGS), Oxford Nanopore, and Sanger sequencing.

## Features

- **Multi-platform support**: Illumina NGS, Oxford Nanopore, Sanger sequencing
- **Multiple input formats**: `.fastq`, `.fasta`, `.ab1`, `.qza`, `.biom`
- **Comprehensive preprocessing**: Quality control, trimming, chimera detection
- **Taxonomic classification**: BLAST, Kraken2, QIIME2 integration
- **Ecological analysis**: Alpha/beta diversity, ordination, clustering
- **Functional predictions**: PICRUSt2 and HUMAnN2 support
- **Rich visualizations**: Interactive and static plots
- **Automated reporting**: PDF/HTML reports
- **Modular design**: Use only what you need

## Installation

### From PyPI (recommended)

```bash
pip install microflex
```

### Development installation

```bash
git clone https://github.com/ataozsoysoy/microflex.git
cd microflex
pip install -e ".[dev]"
```

### Optional dependencies

```bash
# For web interface
pip install "microflex[web]"

# For documentation
pip install "microflex[docs]"

# All optional dependencies
pip install "microflex[dev,web,docs]"
```

## Quick Start

### Python API

```python
from microflex.io import FastqReader
from microflex.preprocess import QualityFilter
from microflex.taxonomy import MockClassifier
from microflex.analysis import DiversityAnalyzer

# Read sequencing data
reader = FastqReader()
sequences = reader.read("data/samples.fastq")

# Quality filtering
quality_filter = QualityFilter(min_quality_score=20, min_length=100)
filtered_sequences = quality_filter.process(sequences)

# Taxonomic classification
classifier = MockClassifier(confidence_range=(70.0, 95.0))
taxonomy_results = classifier.process(filtered_sequences)

# Diversity analysis
analyzer = DiversityAnalyzer()
alpha_metrics = analyzer.calculate_alpha_diversity(abundance_data)
beta_distances = analyzer.calculate_beta_diversity(abundance_matrix)
```

### Command Line Interface

```bash
# Get file information
python -m microflex.cli.main info sequences.fastq

# Filter sequences by quality
python -m microflex.cli.main filter sequences.fastq --min-length 100 --min-quality 20

# Taxonomic classification
python -m microflex.cli.main classify sequences.fasta --method mock

# Diversity analysis
python -m microflex.cli.main analyze taxonomy.tsv --level genus

# Convert between formats
python -m microflex.cli.main convert sequences.fastq --format fasta
```

## Available CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `info` | Display file information | `python -m microflex.cli.main info sequences.fastq` |
| `filter` | Quality-based sequence filtering | `python -m microflex.cli.main filter sequences.fastq --min-length 100` |
| `classify` | Taxonomic classification | `python -m microflex.cli.main classify sequences.fasta --method mock` |
| `analyze` | Diversity analysis | `python -m microflex.cli.main analyze taxonomy.tsv --level genus` |
| `convert` | Format conversion | `python -m microflex.cli.main convert sequences.fastq --format fasta` |

## Project Structure

```
microflex/
├── src/microflex/
│   ├── core/           # Core abstractions and interfaces
│   ├── io/             # Input/output handlers
│   ├── preprocess/     # Quality control and preprocessing
│   ├── taxonomy/       # Taxonomic classification
│   ├── analysis/       # Ecological analysis
│   ├── functional/     # Functional predictions
│   ├── visualization/  # Plotting and visualization
│   ├── cli/            # Command line interface
│   └── utils/          # Utilities and helpers
├── tests/              # Test suite
├── docs/               # Documentation
└── examples/           # Example scripts and notebooks
```

## Documentation

Full documentation is available at [microflex.readthedocs.io](https://microflex.readthedocs.io)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/ataozsoysoy/microflex.git
cd microflex

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run linting
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use microflex in your research, please cite:

```bibtex
@software{microflex,
  author = {Özsoy, Ata Umut},
  title = {microflex: Cross-platform Python toolkit for microbiome analysis},
  url = {https://github.com/ataozsoysoy/microflex},
  version = {0.1.0},
  year = {2025}
}
```

## Roadmap

- [x] v0.1.0: Core architecture, I/O modules, quality filtering, mock classification, alpha/beta diversity, CLI
- [ ] v0.2.0: BLAST integration, Kraken2 support, visualization module
- [ ] v0.3.0: Nanopore support, PICRUSt2 integration, web interface
- [ ] v1.0.0: Stable release with comprehensive documentation and tutorials

## Support

- 📖 [Documentation](https://microflex.readthedocs.io)
- 🐛 [Issue Tracker](https://github.com/ataozsoysoy/microflex/issues)
- 💬 [Discussions](https://github.com/ataozsoysoy/microflex/discussions)

## Acknowledgments

Special thanks to the bioinformatics community and the developers of the underlying tools that make microflex possible. 