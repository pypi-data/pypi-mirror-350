# EvolvisHub Data Handler

<div align="center">
  <img src="assets/png/eviesales.png" alt="Evolvis AI Logo" width="200"/>
</div>

[![PyPI version](https://badge.fury.io/py/evolvishub-data-handler.svg)](https://badge.fury.io/py/evolvishub-data-handler)
[![Python Versions](https://img.shields.io/pypi/pyversions/evolvishub-data-handler.svg)](https://pypi.org/project/evolvishub-data-handler/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/evolvishub/evolvishub-data-handler/actions/workflows/ci.yml/badge.svg)](https://github.com/evolvishub/evolvishub-data-handler/actions/workflows/ci.yml)
[![Code Coverage](https://codecov.io/gh/evolvishub/evolvishub-data-handler/branch/main/graph/badge.svg)](https://codecov.io/gh/evolvishub/evolvishub-data-handler)

A robust Change Data Capture (CDC) library for efficient data synchronization across various databases and storage systems.

## Features

- **Multi-Database Support**: Seamlessly sync data between PostgreSQL, MySQL, SQL Server, Oracle, MongoDB, and more
- **Cloud Storage Integration**: Native support for AWS S3, Google Cloud Storage, and Azure Blob Storage
- **File System Support**: Handle CSV, JSON, and other file formats
- **Watermark Tracking**: Efficient incremental sync with configurable watermark columns
- **Batch Processing**: Optimize performance with configurable batch sizes
- **Error Handling**: Robust error recovery and logging
- **Type Safety**: Full type hints and validation with Pydantic
- **Extensible**: Easy to add new adapters and data sources

## Installation

```bash
# Install from PyPI
pip install evolvishub-data-handler

# Install with development dependencies
pip install evolvishub-data-handler[dev]

# Install with documentation dependencies
pip install evolvishub-data-handler[docs]
```

## Quick Start

1. Create a configuration file (e.g., `config.yaml`):

```yaml
source:
  type: postgresql
  host: localhost
  port: 5432
  database: source_db
  user: source_user
  password: source_password
  watermark:
    column: updated_at
    type: timestamp
    initial_value: "1970-01-01 00:00:00"

destination:
  type: postgresql
  host: localhost
  port: 5432
  database: dest_db
  user: dest_user
  password: dest_password
  watermark:
    column: updated_at
    type: timestamp
    initial_value: "1970-01-01 00:00:00"

sync:
  batch_size: 1000
  interval_seconds: 60
  watermark_table: sync_watermark
```

2. Use the library in your code:

```python
from evolvishub_data_handler import CDCHandler

# Initialize the handler
handler = CDCHandler("config.yaml")

# Run one-time sync
handler.sync()

# Or run continuous sync
handler.run_continuous()
```

3. Or use the command-line interface:

```bash
# One-time sync
evolvishub-cdc -c config.yaml

# Continuous sync
evolvishub-cdc -c config.yaml -m continuous

# With custom logging
evolvishub-cdc -c config.yaml -l DEBUG --log-file sync.log
```

## Supported Data Sources

### Databases
- PostgreSQL
- MySQL
- SQL Server
- Oracle
- MongoDB

### Cloud Storage
- AWS S3
- Google Cloud Storage
- Azure Blob Storage

### File Systems
- CSV files
- JSON files
- Parquet files

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/evolvishub/evolvishub-data-handler.git
cd evolvishub-data-handler
```

2. Create a virtual environment:
```bash
make venv
```

3. Install development dependencies:
```bash
make install
```

4. Install pre-commit hooks:
```bash
make install-hooks
```

### Testing

Run the test suite:
```bash
make test
```

### Code Quality

Format code:
```bash
make format
```

Run linters:
```bash
make lint
```

### Building

Build the package:
```bash
make build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [https://evolvishub.github.io/evolvishub-data-handler](https://evolvishub.github.io/evolvishub-data-handler)
- Issues: [https://github.com/evolvishub/evolvishub-data-handler/issues](https://github.com/evolvishub/evolvishub-data-handler/issues)
- Email: info@evolvishub.com

# EvolvisHub Data Handler Adapter

A powerful and flexible data handling adapter for Evolvis AI's data processing pipeline. This tool provides seamless integration with various database systems and implements Change Data Capture (CDC) functionality.

## About Evolvis AI

[Evolvis AI](https://evolvis.ai) is a leading provider of AI solutions that helps businesses unlock their data potential. We specialize in:

- Data analysis and decision-making
- Machine learning implementation
- Process optimization
- Predictive maintenance
- Natural language processing
- Custom AI solutions

Our mission is to make artificial intelligence accessible to businesses of all sizes, enabling them to compete in today's data-driven environment. As Forbes highlights: "Organizations that strategically adopt AI will have a significant competitive advantage in today's data-driven market."

## Author

**Alban Maxhuni, PhD**  
Email: [a.maxhuni@evolvis.ai](mailto:a.maxhuni@evolvis.ai)