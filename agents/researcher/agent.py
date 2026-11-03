from config.settings import MAX_PRODUCT_DESCRIPTION
from core.llm import LLMClient
from research.fetcher import check_url
from research.sources import classify_source, get_domain


RESEARCHER_INSTRUCTIONS = """
You are the Researcher Agent of a B2B product sales intelligence system.

Your job is to research a product using internet sources.

Rules:

- Search the internet extensively.
- Prefer official product/company sources.
- Use independent sources when useful.
- Never fabricate specifications.
- Every factual claim must have a source URL.
- Clearly distinguish known facts from uncertain information.
- If information is unavailable, say unknown.
- Do not fill missing data with assumptions.
- Keep raw research comprehensive because another agent will clean it.
"""


RESEARCH_SCHEMA = {
    "type": "object",
    "properties": {
        "product_name": {
            "type": "string"
        },
        "overview": {
            "type": "string"
        },
        "facts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "claim": {
                        "type": "string"
                    },
                    "evidence": {
                        "type": "string"
                    },
                    "source_url": {
                        "type": "string"
                    },
                    "confidence": {
                        "type": "string"
                    }
                },
                "required": [
                    "claim",
                    "evidence",
                    "source_url",
                    "confidence"
                ],
                "additionalProperties": False,
            }
        },
        "sources": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string"
                    },
                    "title": {
                        "type": "string"
                    },
                    "domain": {
                        "type": "string"
                    },
                    "source_type": {
                        "type": "string"
                    },
                    "accessible": {
                        "type": "boolean"
                    },
                    "notes": {
                        "type": "string"
                    }
                },
                "required": [
                    "url",
                    "title",
                    "domain",
                    "source_type",
                    "accessible",
                    "notes"
                ],
                "additionalProperties": False,
            }
        }
    },
    "required": [
        "product_name",
        "overview",
        "facts",
        "sources"
    ],
    "additionalProperties": False,
}


def research_product(product):

    client = LLMClient()

    description = (
        product.description
        or "No product description was provided."
    )

    description = description[
        :MAX_PRODUCT_DESCRIPTION
    ]

    prompt = f"""
Research this product:

Product name:
{product.name}

Description:
{description}

Product website:
{product.website or "Not provided"}

Target country:
{product.target_country or "Not provided"}

Research:

- What the product is.
- What it does.
- Main capabilities.
- Technical/product characteristics.
- Who uses it.
- Main applications.
- Relevant industry.
- Commercial positioning.
- Product/company facts.
- Useful competitors.
- Useful market information.

Return all important factual claims and the exact source URL supporting each claim.
"""

    result = client.run(
        instructions=RESEARCHER_INSTRUCTIONS,
        prompt=prompt,
        use_web_search=True,
        schema=RESEARCH_SCHEMA,
    )

    for source in result["sources"]:

        source["domain"] = get_domain(
            source["url"]
        )

        check = check_url(
            source["url"]
        )

        source["accessible"] = check[
            "accessible"
        ]

        source["source_type"] = classify_source(
            source["url"],
            product.website,
        )

    return result