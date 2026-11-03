def rerank_ties(
    ranked_clients,
):

    groups = {}

    for client in ranked_clients:

        score = client["score"]

        groups.setdefault(
            score,
            []
        ).append(client)

    final = []

    for score, group in groups.items():

        if len(group) == 1:
            final.extend(group)
            continue


        group.sort(
            key=lambda item: (
                item["evidence_score"],
                item["industry_score"],
                item["geography_score"],
                item["relevance_score"],
            ),
            reverse=True,
        )

        final.extend(group)

    return final