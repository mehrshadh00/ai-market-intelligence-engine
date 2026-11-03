from models.schemas import Client
from scoring.config import DEFAULT_WEIGHTS
from scoring.scorer import rank_clients, score_client


def make_client(name, *, evidence=None, source_urls=None, country="Germany"):
    return Client(
        name=name,
        country=country,
        field="Industrial AI",
        website="https://example.com",
        reason="Relevant industrial use case.",
        evidence=evidence or [],
        source_urls=source_urls or [],
        evidence_status="verified",
    )


def test_evidence_score_requires_evidence_and_source_url():
    client = make_client(
        "No Source Ltd",
        evidence=["A supporting statement"],
        source_urls=[],
    )
    result = score_client(client, "Germany", DEFAULT_WEIGHTS)
    assert result["evidence_score"] == 0


def test_ranking_is_descending_by_total_score():
    high = make_client("High", evidence=["Evidence"], source_urls=["https://source.test"])
    low = make_client("Low", country="France")
    ranked = rank_clients([low, high], "Germany", DEFAULT_WEIGHTS)
    assert [item["name"] for item in ranked] == ["High", "Low"]


def test_ties_are_broken_deterministically_by_name():
    first = make_client("Zulu")
    second = make_client("Alpha")
    ranked = rank_clients([first, second], "Germany", DEFAULT_WEIGHTS)
    assert [item["name"] for item in ranked] == ["Alpha", "Zulu"]
