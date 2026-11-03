def rerank_ties(ranked_clients):
    """Sort prospects by total score, then apply deterministic tie-breakers."""
    return sorted(
        ranked_clients,
        key=lambda item: (
            -item.get("score", 0),
            -item.get("evidence_score", 0),
            -item.get("industry_score", 0),
            -item.get("geography_score", 0),
            -item.get("relevance_score", 0),
            -item.get("accessibility_score", 0),
            item.get("name", "").casefold(),
        ),
    )
