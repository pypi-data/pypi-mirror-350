"""Async HTTP client for fetching Medium articles."""

import httpx


async def fetch_article(url: str, cookies: dict[str, str] | None = None) -> str:
    """Fetch a Medium article's HTML content.

    Args:
        url: The URL of the Medium article
        cookies: Optional cookies for authentication

    Returns:
        HTML content of the article
    """
    async with httpx.AsyncClient(follow_redirects=True, cookies=cookies) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text
