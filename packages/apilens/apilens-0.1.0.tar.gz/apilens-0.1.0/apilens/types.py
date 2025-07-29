from typing import TypedDict, Optional, Dict, Any, List

class LLMResponse(TypedDict):
    """Standard response format for all LLM providers."""
    choices: List[Dict[str, Any]]
    usage: Optional[Dict[str, int]]
    cost: float

class APILensError(Exception):
    """Base exception for all API Lens errors."""
    pass

class RateLimitError(APILensError):
    """Rate limit exceeded."""
    pass

class AuthError(APILensError):
    """Authentication failed."""
    pass

class BadRequestError(APILensError):
    """Invalid request."""
    pass

class ProviderError(APILensError):
    """Provider-specific error."""
    def __init__(self, provider: str, message: str):
        self.provider = provider
        super().__init__(f"{provider} error: {message}") 