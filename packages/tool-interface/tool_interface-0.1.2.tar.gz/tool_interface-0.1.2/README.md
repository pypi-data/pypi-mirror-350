# tool-interface

Main Python package to access the 3DTrees backend from tool containers. This package provides a unified interface for interacting with various backend services (Supabase, S3) used in the 3DTrees project.

## Installation

From PyPI (recommended):
```bash
pip install tool-interface
```

From GitHub (development version):
```bash
pip install git+https://github.com/3dtrees-earth/tool-interface.git
```

## Configuration

The package uses environment variables for configuration. All variables should be prefixed with `THREEDTREES_`. You can also use a `.env` file.

Required environment variables:
```bash
# Supabase
THREEDTREES_SUPABASE_URL=your_supabase_url
THREEDTREES_SUPABASE_KEY=your_supabase_key

# Storage (S3 compatible)
THREEDTREES_STORAGE_ACCESS_KEY=your_access_key
THREEDTREES_STORAGE_SECRET_KEY=your_secret_key
THREEDTREES_STORAGE_BUCKET_NAME=your_bucket_name

# Optional
THREEDTREES_STORAGE_ENDPOINT_URL=custom_s3_endpoint  # For non-AWS S3
THREEDTREES_STORAGE_REGION=eu-central-1  # Default: eu-central-1
```

## Development

To set up the development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/3dtrees-earth/tool-interface.git
   cd tool-interface
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Code Quality

The project uses several tools to ensure code quality:

- **mypy** for static type checking
- **ruff** for linting and formatting
- **pytest** for testing

Run the checks locally:
```bash
pre-commit run --all-files  # Runs all checks
pytest                      # Runs tests
```

### Versioning

The package uses semantic versioning through git tags. Version numbers are automatically derived from git tags when building the package.

To create a new release:
1. Ensure all changes are committed
2. Create and push a new version tag:
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```
3. The GitHub Actions workflow will automatically build and publish to PyPI

## License

See [LICENSE](LICENSE) file.
