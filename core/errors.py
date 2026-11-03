class AgentError(Exception):
    """Base exception for the sales research system."""


class LLMError(AgentError):
    """Raised when the LLM cannot complete a request."""


class ResearchError(AgentError):
    """Raised when research fails."""


class ExternalServiceError(AgentError):
    """Raised when an external website/service fails."""