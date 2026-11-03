from core.llm import LLMClient


VERIFIER_INSTRUCTIONS = """
You are a source verification specialist.

Your job is NOT to invent facts.

For every claim:
1. Determine whether the supplied evidence actually supports it.
2. Mark it supported, contradicted, or unknown.
3. Never turn unknown into true.
4. If evidence is insufficient, say unknown.
5. Prefer official sources.
"""


def verify_claims(
    claims: list,
    sources: list,
) -> list:

    client = LLMClient()

    prompt = f"""
CLAIMS:

{claims}

SOURCES:

{sources}

Evaluate each claim strictly against the available evidence.

Return JSON:

{{
    "results": [
        {{
            "claim": "...",
            "status": "supported|contradicted|unknown",
            "reason": "...",
            "source_urls": []
        }}
    ]
}}
"""

    result = client.run(
        instructions=VERIFIER_INSTRUCTIONS,
        prompt=prompt,
        use_web_search=True,
    )

    return result.get(
        "results",
        []
    )