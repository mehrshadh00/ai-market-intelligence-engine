from scoring.config import (
    DEFAULT_WEIGHTS,
    validate_weights,
)


def score_client(
    client,
    target_country,
    weights=None,
):

    if weights is None:
        weights = DEFAULT_WEIGHTS

    validate_weights(weights)


    industry_score = 0

    if client.field:
        industry_score = 1


    geography_score = 0

    if (
        target_country
        and client.country
        and client.country.lower()
        == target_country.lower()
    ):
        geography_score = 1



    evidence_score = 0

    if (
        client.evidence_status.lower()
        in {
            "verified",
            "strong",
            "supported",
        }
        and client.evidence
        and client.source_urls
    ):
        evidence_score = 1


    relevance_score = 0

    if client.reason.strip():
        relevance_score = 1



    accessibility_score = 0

    if client.website.strip():
        accessibility_score = 1

    score = (
        industry_score
        * weights["industry"]
        + geography_score
        * weights["geography"]
        + evidence_score
        * weights["evidence"]
        + relevance_score
        * weights["relevance"]
        + accessibility_score
        * weights["accessibility"]
    )

    return {
        "name": client.name,
        "score": round(score, 2),
        "industry_score": industry_score
        * weights["industry"],
        "geography_score": geography_score
        * weights["geography"],
        "evidence_score": evidence_score
        * weights["evidence"],
        "relevance_score": relevance_score
        * weights["relevance"],
        "accessibility_score": accessibility_score
        * weights["accessibility"],
        "evidence_status": (
            client.evidence_status
        ),
        "explanation": (
            "Score generated using deterministic "
            "weighted criteria."
        ),
        "source_urls": client.source_urls,
    }


def rank_clients(
    clients,
    target_country,
    weights=None,
):
    scored = [
        score_client(client, target_country, weights)
        for client in clients
    ]

    from scoring.reranker import rerank_ties

    return rerank_ties(scored)
