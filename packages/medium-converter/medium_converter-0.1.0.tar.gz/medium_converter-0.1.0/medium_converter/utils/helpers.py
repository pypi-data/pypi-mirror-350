"""Helper functions for Medium Converter."""

import os
import re
from urllib.parse import urlparse


def normalize_medium_url(url: str) -> str:
    """Normalize a Medium URL.

    Args:
        url: The URL to normalize

    Returns:
        Normalized URL
    """
    parsed = urlparse(url)

    # Handle medium.com URLs
    if parsed.netloc == "medium.com" or parsed.netloc.endswith(".medium.com"):
        # Remove tracking parameters
        path = parsed.path
        return f"https://{parsed.netloc}{path}"

    # Handle custom domain publications
    # This is simplified and would need to be expanded for all Medium publications
    known_medium_domains = [
        "towardsdatascience.com",
        "betterprogramming.pub",
        "levelup.gitconnected.com",
        "betterhumans.pub",
        "entrepreneurshandbook.co",
        "uxdesign.cc",
    ]

    if parsed.netloc in known_medium_domains or any(
        parsed.netloc.endswith(f".{domain}") for domain in known_medium_domains
    ):
        path = parsed.path
        return f"https://{parsed.netloc}{path}"

    # Return original URL if not recognized
    return url


def safe_filename(filename: str) -> str:
    """Create a safe filename from a string.

    Args:
        filename: The string to convert to a safe filename

    Returns:
        Safe filename
    """
    # Replace spaces with underscores
    s = filename.replace(" ", "_")

    # Remove non-alphanumeric characters except underscores and hyphens
    s = re.sub(r"[^a-zA-Z0-9_-]", "", s)

    # Ensure it's not too long
    if len(s) > 100:
        s = s[:100]

    return s


def get_default_output_path(url: str, title: str, format: str) -> str:
    """Generate a default output path for a converted article.

    Args:
        url: The URL of the article
        title: The title of the article
        format: The output format

    Returns:
        Default output path
    """
    safe_title = safe_filename(title)

    # Get the domain from the URL
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")

    # Create a filename
    filename = f"{safe_title}_{domain}.{format}"

    # Use current directory
    return os.path.join(os.getcwd(), filename)
