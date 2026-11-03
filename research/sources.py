from urllib.parse import urlparse


def get_domain(url: str) -> str:

    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def is_official_source(
    url: str,
    product_website: str | None,
) -> bool:

    if not product_website:
        return False

    product_domain = get_domain(product_website)

    source_domain = get_domain(url)

    if not product_domain or not source_domain:
        return False

    return (
        product_domain == source_domain
        or source_domain.endswith(
            "." + product_domain
        )
    )


def classify_source(
    url: str,
    product_website: str | None,
) -> str:

    if is_official_source(
        url,
        product_website,
    ):
        return "official"

    return "unofficial"