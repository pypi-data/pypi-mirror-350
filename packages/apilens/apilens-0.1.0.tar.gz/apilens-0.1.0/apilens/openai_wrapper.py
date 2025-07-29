import os
import openai
from .config import OPENAI_API_KEY, PRICING
from .base_wrapper import BaseAIWrapper
from .types import LLMResponse, RateLimitError, AuthError, BadRequestError

class OpenAIWrapper(BaseAIWrapper):
    """
    Wraps OpenAI API calls, logs usage, and calculates cost.
    """
    def __init__(self, model="gpt-3.5-turbo", db_path="apilens.db", user_id=None, tenant_id=None, **kwargs):
        if model not in PRICING:
            raise ValueError(f"Unsupported model: {model}. Supported models: {list(PRICING.keys())}")
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment")
        super().__init__(provider_name="openai", model=model, db_path=db_path, user_id=user_id, tenant_id=tenant_id, **kwargs)
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        pricing = PRICING.get(model, {"input": 0.03, "output": 0.06})
        return (prompt_tokens / 1000 * pricing["input"]) + (completion_tokens / 1000 * pricing["output"])

    def _make_api_call(self, messages: list, **kwargs):
        """Make the actual API call to OpenAI."""
        return self.client.chat.completions.create(model=self.model, messages=messages, **kwargs)

    async def _make_async_api_call(self, messages: list, **kwargs):
        """Make an async API call to OpenAI."""
        return await self.client.chat.completions.create(model=self.model, messages=messages, **kwargs)

    def _extract_usage(self, response) -> dict:
        """Extract token usage from OpenAI's response."""
        return {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens
        }

    def _format_response(self, response) -> LLMResponse:
        """Format OpenAI's response into a standard format."""
        return {
            "choices": [{
                "message": {
                    "content": response.choices[0].message.content
                }
            }]
        }

    def _handle_error(self, error: Exception) -> None:
        """Handle OpenAI-specific errors."""
        error_str = str(error).lower()
        if "rate limit" in error_str:
            raise RateLimitError("OpenAI rate limit exceeded")
        elif "authentication" in error_str or "invalid api key" in error_str:
            raise AuthError("OpenAI authentication failed")
        elif "invalid request" in error_str:
            raise BadRequestError(f"OpenAI invalid request: {error_str}")
        raise error

# Future: AnthropicWrapper
