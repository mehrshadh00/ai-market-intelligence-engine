import json
from typing import Any, Dict, Optional

from openai import OpenAI

from config.settings import OPENAI_API_KEY, OPENAI_MODEL
from core.errors import LLMError


class LLMClient:

    def __init__(self):
        if not OPENAI_API_KEY:
            raise LLMError(
                "OPENAI_API_KEY is missing. "
                "Add it to your .env file."
            )

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    def run(
        self,
        instructions: str,
        prompt: str,
        use_web_search: bool = False,
        schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        tools = []

        if use_web_search:
            tools.append(
                {
                    "type": "web_search"
                }
            )

        request = {
            "model": OPENAI_MODEL,
            "instructions": instructions,
            "input": prompt,
            "tools": tools,
        }

        if schema:
            request["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": "agent_result",
                    "strict": True,
                    "schema": schema,
                }
            }

        try:
            response = self.client.responses.create(
                **request
            )

            text = response.output_text.strip()

            if not text:
                raise LLMError(
                    "The model returned an empty response."
                )

            if schema:
                return json.loads(text)

            return {
                "text": text
            }

        except Exception as exc:
            raise LLMError(
                f"OpenAI request failed: {exc}"
            ) from exc