import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4.1-mini",
)


REQUEST_TIMEOUT = 15

MAX_PRODUCT_DESCRIPTION = 5000

MAX_WRITER_CHARACTERS = 1000

TOP_CLIENTS_FOR_EMAIL = 2

MARKET_ANALYSIS_STEPS = 5