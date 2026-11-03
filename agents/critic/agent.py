from core.llm import LLMClient


CRITIC_INSTRUCTIONS = """
You are the Critic Agent.

You receive raw product research.

Your job is to identify:

- unsupported claims
- weak evidence
- missing information
- duplicated information
- unclear statements
- poor source quality
- contradictions
- areas requiring stronger sources

Do NOT rewrite the final product description.

Be conservative.

Unknown information must remain unknown.
"""


CRITIC_SCHEMA = {
    "type": "object",
    "properties": {
        "strengths": {
            "type": "array",
            "items": {"type": "string"}
        },
        "weaknesses": {
            "type": "array",
            "items": {"type": "string"}
        },
        "missing_information": {
            "type": "array",
            "items": {"type": "string"}
        },
        "unsupported_claims": {
            "type": "array",
            "items": {"type": "string"}
        },
        "recommendations": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": [
        "strengths",
        "weaknesses",
        "missing_information",
        "unsupported_claims",
        "recommendations"
    ],
    "additionalProperties": False,
}


def critique_research(
    research: dict,
):

    client = LLMClient()

    prompt = f"""
Here is the raw research:

{research}

Critically evaluate it.

Pay special attention to:
1. Unsupported factual claims.
2. Claims with no source.
3. Duplicate information.
4. Weak or unofficial evidence.
5. Missing product information.
6. Claims that should be removed from the final overview.
7. Claims that should be qualified as uncertain.
"""

    return client.run(
        instructions=CRITIC_INSTRUCTIONS,
        prompt=prompt,
        use_web_search=True,
        schema=CRITIC_SCHEMA,
    )