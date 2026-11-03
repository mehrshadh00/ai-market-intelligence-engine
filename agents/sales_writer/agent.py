from core.llm import LLMClient


SALES_WRITER_INSTRUCTIONS = """
You are a professional B2B sales email writer.

Create a highly personalized sales email.

The email must:

- mention the client by name
- relate directly to their field
- explain why the product could matter to them
- avoid generic mass-sales language
- avoid unsupported claims
- remain professional
- have a clear call to action
- be concise
"""


EMAIL_SCHEMA = {
    "type": "object",
    "properties": {
        "client_name": {
            "type": "string"
        },
        "subject": {
            "type": "string"
        },
        "body": {
            "type": "string"
        }
    },
    "required": [
        "client_name",
        "subject",
        "body"
    ],
    "additionalProperties": False,
}


def generate_sales_email(
    product,
    client,
    product_overview,
):

    llm = LLMClient()

    prompt = f"""
PRODUCT:

{product}

PRODUCT OVERVIEW:

{product_overview}

TARGET CLIENT:

{client}

Write a personalized B2B sales email.

The email should feel like it was specifically
written for this company.
"""

    return llm.run(
        instructions=SALES_WRITER_INSTRUCTIONS,
        prompt=prompt,
        use_web_search=True,
        schema=EMAIL_SCHEMA,
    )