from typing import Optional

import requests

from config.settings import REQUEST_TIMEOUT


def check_url(url: str) -> dict:

    if not url:
        return {
            "accessible": False,
            "status_code": None,
            "error": "Empty URL",
        }

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(ProductResearchAgent/1.0)"
                )
            },
            allow_redirects=True,
        )

        return {
            "accessible": response.ok,
            "status_code": response.status_code,
            "final_url": response.url,
            "error": None,
        }

    except requests.RequestException as exc:

        return {
            "accessible": False,
            "status_code": None,
            "final_url": url,
            "error": str(exc),
        }


def fetch_page(url: str) -> Optional[str]:

    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(ProductResearchAgent/1.0)"
                )
            },
        )

        response.raise_for_status()

        return response.text

    except requests.RequestException:
        return None