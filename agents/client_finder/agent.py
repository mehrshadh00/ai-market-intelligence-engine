from core.llm import LLMClient


CLIENT_FINDER_INSTRUCTIONS = """
You are the Client Finder Agent.

Find exactly 5 potential B2B clients.

Rules:

1. Clients must plausibly need the product.
2. Remove duplicates.
3. Separate verified facts from potential assumptions.
4. Never fabricate company information.
5. Include country.
6. Include field of work.
7. Include website.
8. Explain why the company fits.
9. Provide evidence.
10. Provide source URLs.
11. If evidence is weak, mark the client as potential.
12. Do not give positive certainty without evidence.
"""


CLIENT_SCHEMA = {
    "type": "object",
    "properties": {
        "clients": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "country": {"type": "string"},
                    "field": {"type": "string"},
                    "website": {"type": "string"},
                    "reason": {"type": "string"},
                    "evidence": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "source_urls": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "evidence_status": {
                        "type": "string"
                    }
                },
                "required": [
                    "name",
                    "country",
                    "field",
                    "website",
                    "reason",
                    "evidence",
                    "source_urls",
                    "evidence_status"
                ],
                "additionalProperties": False
            }
        }
    },
    "required": ["clients"],
    "additionalProperties": False,
}


def find_clients(
    product,
    market_analysis,
    provider_analysis,
):

    client = LLMClient()

    prompt = f"""
PRODUCT:

{product}

MARKET ANALYSIS:

{market_analysis}

PROVIDER ANALYSIS:

{provider_analysis}

Find exactly five potential clients.

They must actually fit the product.

Avoid:
- companies with no evidence
- duplicates
- irrelevant industries
- companies outside the chosen geography

For each client provide evidence and source URLs.
"""

    return client.run(
        instructions=CLIENT_FINDER_INSTRUCTIONS,
        prompt=prompt,
        use_web_search=True,
        schema=CLIENT_SCHEMA)