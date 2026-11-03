from scoring.reranker import rerank_ties


def test_tied_clients_are_reranked():

    clients = [

        {
            "name": "Company A",
            "score": 70,
            "evidence_score": 20,
            "industry_score": 30,
            "geography_score": 10,
            "relevance_score": 10,
        },

        {
            "name": "Company B",
            "score": 70,
            "evidence_score": 30,
            "industry_score": 20,
            "geography_score": 10,
            "relevance_score": 10,
        },
    ]

    result = rerank_ties(
        clients
    )

    assert result[0]["name"] == (
        "Company B"
    )

def test_rank_clients_uses_tie_breaker():
    from models.schemas import Client
    from scoring.scorer import rank_clients

    clients = [
        Client(
            name="Geography-first",
            country="Germany",
            field="AI",
            website="https://example.com",
            reason="Relevant prospect.",
            evidence=[],
            source_urls=[],
            evidence_status="unknown",
        ),
        Client(
            name="Evidence-first",
            country="France",
            field="AI",
            website="https://example.org",
            reason="Relevant prospect.",
            evidence=["Official source confirms relevance."],
            source_urls=["https://example.org"],
            evidence_status="verified",
        ),
    ]
    weights = {
        "industry": 20,
        "geography": 20,
        "evidence": 20,
        "relevance": 20,
        "accessibility": 20,
    }

    ranked = rank_clients(clients, "Germany", weights)

    assert ranked[0]["name"] == "Evidence-first"
