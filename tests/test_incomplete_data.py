from models.schemas import Client
from scoring.scorer import score_client


def test_unknown_evidence_gets_zero():

    client = Client(
        name="Unknown Company",
        country="Germany",
        field="Medical AI",
        website="https://example.com",
        reason="Potentially relevant.",
        evidence=[],
        source_urls=[],
        evidence_status="unknown",
    )

    weights = {
        "industry": 30,
        "geography": 20,
        "evidence": 30,
        "relevance": 10,
        "accessibility": 10,
    }

    result = score_client(
        client,
        "Germany",
        weights,
    )

    assert result[
        "evidence_score"
    ] == 0