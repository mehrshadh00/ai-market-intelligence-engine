def rerank_ties(ranked_clients):
    """Sort prospects by total score, then apply deterministic tie-breakers."""
    return sorted(
        ranked_clients,
        key=lambda item: (
            -item["score"],
            -item["evidence_score"],
            -item["industry_score"],
            -item["geography_score"],
            -item["relevance_score"],
            -item["accessibility_score"],
            item["name"].casefold(),
        ),
    )
