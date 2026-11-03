from typing import List, Optional

from pydantic import BaseModel, Field


class ProductInput(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    target_country: Optional[str] = None


class Source(BaseModel):
    url: str
    title: str = ""
    domain: str = ""
    source_type: str = "unofficial"
    accessible: bool = False
    notes: str = ""


class ResearchItem(BaseModel):
    claim: str
    evidence: str = ""
    source_url: str = ""
    confidence: str = "unknown"


class ResearchResult(BaseModel):
    product_name: str
    overview: str
    facts: List[ResearchItem] = Field(default_factory=list)
    sources: List[Source] = Field(default_factory=list)


class CriticResult(BaseModel):
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    unsupported_claims: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class WriterResult(BaseModel):
    product_overview: str
    sources: List[Source] = Field(default_factory=list)


class Company(BaseModel):
    name: str
    country: str
    website: str
    field: str
    reason: str = ""
    sources: List[str] = Field(default_factory=list)


class MarketAnalysis(BaseModel):
    target_countries: List[str] = Field(default_factory=list)
    competitors: List[Company] = Field(default_factory=list)
    reasoning: str = ""
    sources: List[Source] = Field(default_factory=list)


class Client(BaseModel):
    name: str
    country: str
    field: str
    website: str
    reason: str
    evidence: List[str] = Field(default_factory=list)
    source_urls: List[str] = Field(default_factory=list)
    evidence_status: str = "potential"


class ClientList(BaseModel):
    clients: List[Client] = Field(default_factory=list)


class ClientScore(BaseModel):
    name: str
    score: float
    industry_score: float
    geography_score: float
    evidence_score: float
    relevance_score: float
    accessibility_score: float
    evidence_status: str
    explanation: str
    source_urls: List[str] = Field(default_factory=list)


class SalesEmail(BaseModel):
    client_name: str
    subject: str
    body: str