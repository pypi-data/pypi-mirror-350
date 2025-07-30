# Media Transcoder

A powerful media transcoding tool with CUDA hardware acceleration support.

## Features

- Transcode video files to web-optimized formats
- NVIDIA CUDA hardware acceleration support for faster transcoding
- Automatic detection of hardware capabilities
- Batch processing of media files
- Database tracking of transcoded files
- Web-safe filename generation

## Installation

```bash
# Using uv (recommended)
uv pip install media-transcoder

# Using pip
pip install media-transcoder
```

## Requirements

- Python 3.8+
- FFmpeg with hardware acceleration support (optional)
- NVIDIA GPU with CUDA support (optional, for hardware acceleration)

## Usage

```bash
# Basic usage
media-transcoder -t /path/to/videos/

# Use hardware acceleration (if available)
media-transcoder -t /path/to/videos/ --keep-originals

# Force software encoding
media-transcoder -t /path/to/videos/ --software-only

# Generate web-safe filenames
media-transcoder -t /path/to/videos/ --web-safe-names

# Verbose output
media-transcoder -t /path/to/videos/ -v

# Force processing of all files
media-transcoder -t /path/to/videos/ -f
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/lpetrov/media-transcoder.git
cd media-transcoder

# Install development dependencies using uv
uv pip install -e ".[dev]"
```

### Run Tests

```bash
# Using uv
uv run pytest

# Or with the script runner
uv run --script tests/test_transcoder.py
```

### Run Tests with Coverage

```bash
# Using uv
uv run pytest --cov=media_transcoder
```

### Building the Package

To build the package for distribution:

```bash
# Build both wheel and source distribution
uv build

# The built packages will be in the dist/ directory
ls dist/
```

### Publishing to PyPI

To publish the package to PyPI:

```bash
# Test publishing to TestPyPI first
uv publish --index testpypi

# Publish to the official PyPI
uv publish
```

### Managing Dependencies

This project uses UV for dependency management. To update dependencies:

```bash
# Update all dependencies
uv pip sync

# Add a new dependency
uv pip install new-package
```

## License

MIT
