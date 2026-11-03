from urllib.parse import urlparse


def valid_http_url(url: str) -> bool:

    if not url:
        return False

    try:

        parsed = urlparse(url)

        return parsed.scheme in {
            "http",
            "https",
        } and bool(parsed.netloc)

    except Exception:

        return False