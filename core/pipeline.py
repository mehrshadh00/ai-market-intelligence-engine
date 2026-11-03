import os
import json
import re

from dotenv import load_dotenv
from openai import OpenAI
from models.schemas import ProductInput
from scoring.config import validate_weights

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def _ask(client, prompt, web_search=False):
    kwargs = {
        "model": MODEL,
        "input": prompt,
    }
    if web_search:
        kwargs["tools"] = [{"type": "web_search"}]

    response = client.responses.create(**kwargs)
    return response


def _citations(response):
    found = []
    for item in getattr(response, "output", []):
        if getattr(item, "type", None) != "message":
            continue
        for part in getattr(item, "content", []):
            for ann in getattr(part, "annotations", []) or []:
                if getattr(ann, "type", None) == "url_citation":
                    url = getattr(ann, "url", None)
                    title = getattr(ann, "title", None) or url
                    if url and not any(s["url"] == url for s in found):
                        found.append({
                            "url": url,
                            "title": title,
                            "source_type": "web",
                            "accessible": True,
                        })
    return found


def _json_from_text(text):
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("The model did not return valid JSON.")
    return json.loads(match.group())


def run_pipeline(product: ProductInput, weights: dict, progress_callback=None):
    validate_weights(weights)

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to the project's .env file."
        )

    client = OpenAI()
    name = product.name.strip()
    description = product.description or ""
    website = product.website or ""
    country = product.target_country or "Not specified"

    def progress(message):
        if progress_callback:
            progress_callback(message)

    progress("Research agent: searching the web...")
    research_response = _ask(
        client,
        f"""
Research this product for sales intelligence.

Product: {name}
Description: {description}
Website supplied by user: {website}
Target country: {country}

Search the web for the product's actual features and use cases, relevant
market trends, competitors, and real organizations that could plausibly buy
it in the target country. Prioritize official company pages and credible
sources. Distinguish verified facts from hypotheses. Do not invent URLs,
companies, statistics, or quotes. Provide a concise research report with
source citations. If the product is ambiguous, say so.
""",
        web_search=True,
    )
    research_text = research_response.output_text
    sources = _citations(research_response)

    if not research_text.strip():
        raise RuntimeError("Web research returned no text.")


    progress("Critic and analyst agents: evaluating evidence...")
    analysis_response = _ask(
        client,
        f"""
You are a sales-intelligence analyst. Use ONLY the research report below
as factual evidence. Never invent facts, sources, URLs, or email addresses.

PRODUCT
Name: {name}
Description: {description}
Website: {website}
Target country: {country}

RESEARCH REPORT:
{research_text}

Return ONLY one valid JSON object with exactly these keys:
{{
  "product_overview": "Clear product overview; distinguish verified facts from unknowns",
  "weaknesses": ["Evidence gaps and limitations"],
  "unsupported_claims": ["Claims not supported by the research"],
  "market_steps": ["Four concise market-analysis steps/findings"],
  "provider": "Reasoning about relevant suppliers/providers, or state insufficient evidence",
  "clients": [
    {{
      "name": "Real organization found in the research",
      "country": "Country or Unknown",
      "field": "Industry",
      "website": "Official URL or empty string",
      "evidence_status": "verified, supported, or unknown",
      "reason": "Why this organization could be a customer",
      "evidence": ["Specific supporting evidence from the research"],
      "source_urls": ["Only URLs explicitly present in the research"]
    }}
  ],
  "sales_emails": [
    {{
      "client_name": "Exact organization name from clients",
      "subject": "Personalized subject",
      "body": "Professional, truthful outreach email"
    }}
  ]
}}

Only include real prospects supported by the research. If there is not enough
evidence, return empty clients and sales_emails arrays rather than guessing.
Do not invent direct contacts or imply a prospect has expressed interest.
Generate an email only for an included prospect. Keep emails personalized
but do not claim facts that the research does not support.
""",
    )
    data = _json_from_text(analysis_response.output_text)

    progress("Ranking agent: calculating weighted prospect scores...")
    ranked = []
    for raw in data.get("clients", []):
        country_match = (
            bool(country and country != "Not specified")
            and raw.get("country", "").casefold() == country.casefold()
        )
        industry = bool(raw.get("field"))
        evidence = (
            raw.get("evidence_status", "").casefold()
            in {"verified", "supported", "strong"}
            and bool(raw.get("evidence"))
            and bool(raw.get("source_urls"))
        )
        relevance = bool(raw.get("reason", "").strip())
        accessibility = bool(raw.get("website", "").strip())

        parts = {
            "industry_score": weights["industry"] if industry else 0,
            "geography_score": weights["geography"] if country_match else 0,
            "evidence_score": weights["evidence"] if evidence else 0,
            "relevance_score": weights["relevance"] if relevance else 0,
            "accessibility_score": weights["accessibility"] if accessibility else 0,
        }
        raw["score"] = round(sum(parts.values()), 2)
        raw.update(parts)
        raw["explanation"] = (
            "Deterministic weighted score. A nonzero evidence score requires "
            "supporting evidence and at least one cited source URL."
        )
        ranked.append(raw)

    ranked.sort(key=lambda x: (-x["score"], x["name"].casefold()))

    progress("Pipeline completed.")
    return {
        "writer": {
            "product_overview": data.get("product_overview", ""),
        },
        "research": {
            "sources": sources,
        },
        "critic": {
            "weaknesses": data.get("weaknesses", []),
            "unsupported_claims": data.get("unsupported_claims", []),
        },
        "market_steps": data.get("market_steps", []),
        "provider": data.get("provider", ""),
        "clients": {
            "clients": data.get("clients", []),
        },
        "ranking": ranked,
        "sales_emails": data.get("sales_emails", []),
    }
