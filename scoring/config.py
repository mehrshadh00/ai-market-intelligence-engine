DEFAULT_WEIGHTS = {
    "industry": 30,
    "geography": 20,
    "evidence": 30,
    "relevance": 10,
    "accessibility": 10,
}


def validate_weights(weights: dict):

    required = set(
        DEFAULT_WEIGHTS.keys()
    )

    if set(weights.keys()) != required:
        raise ValueError(
            "Weights must contain exactly: "
            + ", ".join(required)
        )

    if any(
        value < 0
        for value in weights.values()
    ):
        raise ValueError(
            "Weights cannot be negative."
        )

    if sum(weights.values()) != 100:
        raise ValueError(
            "Weights must sum to 100."
        )