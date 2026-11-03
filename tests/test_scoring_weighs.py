from models.schemas import Client
from scoring.scorer import score_client


def make_client():

    return Client(
        name="Test Company",
        country="Germany",
        field="Medical AI",
        website="https://example.com",
        reason="The company operates in the relevant field.",
        evidence=[
            "Official website confirms relevant activity."
        ],
        source_urls=[
            "https://example.com"
        ],
        evidence_status="verified",
    )


def test_weights_change_score():

    client = make_client()

    weights_a = {
        "industry": 50,
        "geography": 10,
        "evidence": 20,
        "relevance": 10,
        "accessibility": 10,
    }

    weights_b = {
        "industry": 10,
        "geography": 50,
        "evidence": 20,
        "relevance": 10,
        "accessibility": 10,
    }

    score_a = score_client(
        client,
        "France",
        weights_a,
    )

    score_b = score_client(
        client,
        "France",
        weights_b,
    )

    assert score_a["score"] != score_b["score"]