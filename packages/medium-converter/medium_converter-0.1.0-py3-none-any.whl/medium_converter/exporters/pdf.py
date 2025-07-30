"""PDF exporter for Medium articles."""

from typing import BinaryIO, TextIO

from ..core.models import Article
from .base import BaseExporter


class PDFExporter(BaseExporter):
    """Export Medium articles to PDF format."""

    def export(
        self, article: Article, output: str | TextIO | BinaryIO | None = None
    ) -> bytes:
        """Export an article to PDF.

        Args:
            article: The article to export
            output: Optional output file path or file-like object

        Returns:
            The exported content as bytes
        """
        try:
            from io import BytesIO

            # reportlab imports
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
            from reportlab.lib.units import inch
            from reportlab.platypus import (
                Paragraph,
                SimpleDocTemplate,
                Spacer,
            )
        except ImportError as err:
            raise ImportError(
                "PDF export requires reportlab."
                "Install with 'pip install medium-converter[pdf]'"
            ) from err

        # Create a buffer for the PDF
        buffer = BytesIO()

        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer if output is None else output if isinstance(output, str) else buffer,
            pagesize=A4,
            title=article.title,
            author=article.author,
        )

        # Get styles
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        styles["Heading1"]
        styles["Heading2"]
        normal_style = styles["Normal"]

        # Create PDF elements
        elements = []

        # Add title
        elements.append(Paragraph(article.title, title_style))
        elements.append(Spacer(1, 0.2 * inch))

        # Add author and date
        elements.append(
            Paragraph(f"By {article.author} | {article.date}", normal_style)
        )
        elements.append(Spacer(1, 0.2 * inch))

        # Add reading time if available
        if article.estimated_reading_time:
            elements.append(
                Paragraph(
                    f"{article.estimated_reading_time} min read",
                    ParagraphStyle(
                        "Italic", parent=normal_style, textColor=colors.gray
                    ),
                )
            )
            elements.append(Spacer(1, 0.2 * inch))

        # Example code to process content (placeholder)
        elements.append(
            Paragraph(
                "Content will be rendered here in the actual implementation",
                normal_style,
            )
        )

        # Build the PDF
        doc.build(elements)

        # Get the PDF content
        pdf_content = buffer.getvalue()
        buffer.close()

        # Write to file if specified and not already written
        if output and isinstance(output, str):
            with open(output, "wb") as f:
                f.write(pdf_content)

        return pdf_content
