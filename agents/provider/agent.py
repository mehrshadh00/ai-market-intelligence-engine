from core.llm import LLMClient


PROVIDER_INSTRUCTIONS = """
You are the Provider Analysis Agent.

You receive market research and a selected group
of companies.

Explain why the companies were selected.

Focus on objective similarities:

- product category
- technical capability
- industry
- target customers
- geographic market
- use cases

Do not claim something is true without evidence.
"""


def explain_competitors(
    product,
    market_analysis,
):

    client = LLMClient()

    prompt = f"""
PRODUCT:

{product}

MARKET ANALYSIS:

{market_analysis}

Explain why the final five companies
are appropriate competitors/providers.

Give a short reasoning for each company.

Include source URLs.
"""

    return client.run(
        instructions=PROVIDER_INSTRUCTIONS,
        prompt=prompt,
        use_web_search=True,
    )["text"]