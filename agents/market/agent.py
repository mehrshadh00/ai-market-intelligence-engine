from core.llm import LLMClient


MARKET_INSTRUCTIONS = """
You are a B2B Market Analysis Agent.

Your job is to analyze where a product could be sold
and which companies are relevant competitors.

Never invent companies.

Every company should have evidence.

Unknown information must remain unknown.

Prefer official company websites.
"""


def run_market_step(
    product,
    research,
    previous_steps,
    step_number,
):

    client = LLMClient()

    if step_number == 1:

        task = """
Identify 5 geographical markets/countries
where this product could realistically be sold.

Consider:
- industry
- demand
- product relevance
- technological maturity
- target country if supplied
"""

    elif step_number == 2:

        task = """
Identify 5 companies that manufacture,
develop, distribute or offer products
similar to the target product.
"""

    elif step_number == 3:

        task = """
For each competitor provide:

- company name
- country
- website
- field of work
- similarity to target product
- source
"""

    elif step_number == 4:

        task = """
Compare the competitors.

Explain:
- product similarities
- market similarities
- technological similarities
- customer similarities
"""
    else:

        task = """
Produce the final market analysis.

Select the strongest 5 competitors
and explain why these five were selected.
"""

    prompt = f"""
PRODUCT:

{product}

RESEARCH:

{research}

PREVIOUS MARKET STEPS:

{previous_steps}

CURRENT STEP:

{step_number}

TASK:

{task}

Return a structured analysis with source URLs.
"""

    result = client.run(
        instructions=MARKET_INSTRUCTIONS,
        prompt=prompt,
        use_web_search=True,
    )

    return result["text"]