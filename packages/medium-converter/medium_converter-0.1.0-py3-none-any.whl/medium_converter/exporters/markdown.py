"""Markdown exporter for Medium articles."""

from typing import BinaryIO, TextIO

from ..core.models import Article, ContentBlock, ContentType, Section
from .base import BaseExporter


class MarkdownExporter(BaseExporter):
    """Export Medium articles to Markdown format."""

    def export(
        self, article: Article, output: str | TextIO | BinaryIO | None = None
    ) -> str:
        """Export an article to Markdown.

        Args:
            article: The article to export
            output: Optional output file path or file-like object

        Returns:
            The exported content as string
        """
        md_content = f"# {article.title}\n\n"
        md_content += f"By {article.author} | {article.date}\n\n"

        if article.tags:
            tags = ", ".join([f"#{tag.replace(' ', '')}" for tag in article.tags])
            md_content += f"{tags}\n\n"

        if article.estimated_reading_time:
            md_content += f"*{article.estimated_reading_time} min read*\n\n"

        # Process content
        for item in article.content:
            if isinstance(item, Section):
                if item.title:
                    md_content += f"## {item.title}\n\n"

                for block in item.blocks:
                    md_content += self._format_block(block)
            elif isinstance(item, ContentBlock):
                md_content += self._format_block(item)

        # Write to file if specified
        if output:
            if isinstance(output, str):
                with open(output, "w", encoding="utf-8") as f:
                    f.write(md_content)
            else:
                # We need to check the type to avoid mypy errors
                if hasattr(output, "write") and callable(output.write):
                    if isinstance(output, BinaryIO):
                        output.write(md_content.encode("utf-8"))
                    else:
                        # Assume TextIO
                        output.write(md_content)

        return md_content

    def _format_block(self, block: ContentBlock) -> str:
        """Format a content block as Markdown.

        Args:
            block: The content block to format

        Returns:
            Markdown-formatted string for the block
        """
        if block.type == ContentType.TEXT:
            return f"{block.content}\n\n"
        elif block.type == ContentType.HEADING:
            level = block.metadata.get("level", 2)
            hashes = "#" * level
            return f"{hashes} {block.content}\n\n"
        elif block.type == ContentType.IMAGE:
            alt = block.metadata.get("alt", "")
            return f"![{alt}]({block.content})\n\n"
        elif block.type == ContentType.CODE:
            lang = block.metadata.get("language", "")
            return f"```{lang}\n{block.content}\n```\n\n"
        elif block.type == ContentType.QUOTE:
            return f"> {block.content}\n\n"
        elif block.type == ContentType.LIST:
            list_type = block.metadata.get("list_type", "unordered")
            items = block.content.split("\n")
            result = ""

            for i, item in enumerate(items):
                if list_type == "ordered":
                    result += f"{i + 1}. {item}\n"
                else:
                    result += f"- {item}\n"

            return result + "\n"
        else:
            return f"{block.content}\n\n"
