import re


def normalize_text(text: str) -> str:

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def remove_duplicate_strings(
    items: list[str],
) -> list[str]:

    seen = set()

    result = []

    for item in items:

        normalized = normalize_text(
            item
        )

        if normalized in seen:
            continue

        seen.add(normalized)

        result.append(item)

    return result