# AI Market Intelligence Engine

An AI-powered workflow for researching a product, analyzing its market, discovering potential business clients, ranking prospects with explainable criteria, and drafting personalized outreach emails.

## Features

- Web research using the OpenAI API and web search
- Critique of unsupported claims and missing evidence
- Market and competitor analysis
- Potential-client discovery
- Deterministic, configurable prospect scoring
- Personalized sales-email drafting and optional SMTP delivery
- Unit tests for scoring, incomplete evidence, and tie-breaking

## Architecture

```text
Product Brief
    ↓
Web Research → Evidence Critique
    ↓
Market Analysis → Potential-Client Discovery
    ↓
Deterministic Scoring → Ranked Prospects
    ↓
Email Drafting → Optional SMTP Delivery
```

## Tech Stack

Python · Streamlit · OpenAI Responses API · Pydantic · python-dotenv · Pytest · SMTP

## Quick Start

### 1. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and add your own credentials:

```dotenv
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
```

SMTP variables in `.env.example` are optional and are needed only if you want to send emails from the application. Use a Gmail App Password rather than your regular account password.

### 4. Run the application

```bash
streamlit run app.py
```

### 5. Run tests

```bash
python -m pytest -v
```

## Explainable Prospect Scoring

Prospects are scored in Python using configurable weights across five criteria:

- Industry relevance
- Geographic match
- Supporting evidence
- Business relevance
- Website accessibility

The scoring logic is deterministic, making the ranking easier to inspect and test than an LLM-generated score. Missing or unverified evidence is not treated as a positive signal.

## Security Notes

- Never commit `.env`, API keys, SMTP credentials, or private datasets.
- Review generated research and verify prospects before contacting them.
- Review every generated email and recipient before sending.
- API usage may incur costs.

## Project Status

This is a portfolio project. The included tests cover core scoring behavior; they do not constitute full end-to-end or production-readiness validation.
