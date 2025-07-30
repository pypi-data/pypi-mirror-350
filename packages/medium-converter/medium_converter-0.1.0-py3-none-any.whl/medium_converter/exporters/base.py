"""Base exporter for Medium articles."""

from abc import ABC, abstractmethod
from typing import BinaryIO, TextIO

from ..core.models import Article


class BaseExporter(ABC):
    """Base class for all exporters."""

    @abstractmethod
    def export(
        self, article: Article, output: str | TextIO | BinaryIO | None = None
    ) -> str | bytes:
        """Export an article to the target format.

        Args:
            article: The article to export
            output: Optional output file path or file-like object

        Returns:
            The exported content as string or bytes
        """
        pass
