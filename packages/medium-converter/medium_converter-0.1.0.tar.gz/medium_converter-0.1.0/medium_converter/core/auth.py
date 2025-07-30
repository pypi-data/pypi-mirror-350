"""Authentication utilities for Medium."""

import browser_cookie3


def get_medium_cookies() -> dict[str, str]:
    """Extract Medium cookies from the user's browser.

    Returns:
        Dict of cookies for Medium domain
    """
    try:
        cookies = browser_cookie3.chrome(domain_name="medium.com")
        return {cookie.name: cookie.value for cookie in cookies}
    except Exception:
        # Fallback to Firefox
        try:
            cookies = browser_cookie3.firefox(domain_name="medium.com")
            return {cookie.name: cookie.value for cookie in cookies}
        except Exception:
            return {}
