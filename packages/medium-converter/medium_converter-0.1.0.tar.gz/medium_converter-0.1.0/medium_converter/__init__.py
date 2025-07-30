"""Medium Converter - Convert articles to various formats with LLM enhancement."""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("medium-converter")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.1.0"  # Default during development
