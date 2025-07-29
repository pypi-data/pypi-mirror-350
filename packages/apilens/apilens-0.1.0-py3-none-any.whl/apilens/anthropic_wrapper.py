import os
import anthropic
from .config import ANTHROPIC_API_KEY, PRICING
from .base_wrapper import BaseAIWrapper
from .types import LLMResponse, RateLimitError, AuthError, BadRequestError

class AnthropicWrapper(BaseAIWrapper):
    """
    Wraps Anthropic API calls, logs usage, and calculates cost.
    """
    def __init__(self, model="claude-3-opus-20240229", db_path="apilens.db", user_id=None, tenant_id=None, **kwargs):
        if model not in PRICING:
            raise ValueError(f"Unsupported model: {model}. Supported models: {list(PRICING.keys())}")
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")
        super().__init__(provider_name="anthropic", model=model, db_path=db_path, user_id=user_id, tenant_id=tenant_id, **kwargs)
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def _make_api_call(self, messages: list, **kwargs):
        """Make the actual API call to Anthropic."""
        # Extract system message if present
        system_message = None
        filtered_messages = []
        
        for msg in messages:
            if msg.get("role") == "system":
                system_message = msg.get("content")
            else:
                filtered_messages.append(msg)
        
        # Prepare API parameters
        api_params = {
            "model": self.model,
            "messages": filtered_messages,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": kwargs.get("temperature", 1.0)
        }
        
        if system_message:
            api_params["system"] = system_message
            
        return self.client.messages.create(**api_params)

    async def _make_async_api_call(self, messages: list, **kwargs):
        """Make an async API call to Anthropic."""
        # Extract system message if present
        system_message = None
        filtered_messages = []
        
        for msg in messages:
            if msg.get("role") == "system":
                system_message = msg.get("content")
            else:
                filtered_messages.append(msg)
        
        # Prepare API parameters
        api_params = {
            "model": self.model,
            "messages": filtered_messages,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "temperature": kwargs.get("temperature", 1.0)
        }
        
        if system_message:
            api_params["system"] = system_message
            
        return await self.client.messages.create(**api_params)

    def _extract_usage(self, response) -> dict:
        """Extract token usage from Anthropic's response."""
        return {
            "prompt_tokens": response.usage.input_tokens,
            "completion_tokens": response.usage.output_tokens
        }

    def _format_response(self, response) -> LLMResponse:
        """Format Anthropic's response into a standard format."""
        return {
            "choices": [{
                "message": {
                    "content": response.content[0].text
                }
            }]
        }

    def _handle_error(self, error: Exception) -> None:
        """Handle Anthropic-specific errors."""
        error_str = str(error).lower()
        if "rate limit" in error_str:
            raise RateLimitError("Anthropic rate limit exceeded")
        elif "authentication" in error_str or "invalid api key" in error_str:
            raise AuthError("Anthropic authentication failed")
        elif "invalid request" in error_str:
            raise BadRequestError(f"Anthropic invalid request: {error_str}")
        raise error 