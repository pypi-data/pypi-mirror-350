import os
import google.generativeai as genai
from .config import GEMINI_API_KEY, PRICING
from .base_wrapper import BaseAIWrapper
from .types import LLMResponse, RateLimitError, AuthError, BadRequestError

class GeminiWrapper(BaseAIWrapper):
    """
    Wraps Google's Gemini API calls, logs usage, and calculates cost.
    """
    def __init__(self, model="gemini-pro", db_path="apilens.db", user_id=None, tenant_id=None, **kwargs):
        if model not in PRICING:
            raise ValueError(f"Unsupported model: {model}. Supported models: {list(PRICING.keys())}")
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set in environment")
        super().__init__(provider_name="gemini", model=model, db_path=db_path, user_id=user_id, tenant_id=tenant_id, **kwargs)
        genai.configure(api_key=GEMINI_API_KEY)
        self.client = genai.GenerativeModel(model_name=model)

    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        pricing = PRICING.get(model, {"input": 0.01, "output": 0.02})
        return (prompt_tokens / 1000 * pricing["input"]) + (completion_tokens / 1000 * pricing["output"])

    def _make_api_call(self, messages: list, **kwargs):
        """Make the actual API call to Gemini."""
        prompt = self._convert_messages_to_prompt(messages)
        return self.client.generate_content(prompt, generation_config=self._get_generation_config(**kwargs))

    async def _make_async_api_call(self, messages: list, **kwargs):
        """Make an async API call to Gemini."""
        prompt = self._convert_messages_to_prompt(messages)
        return await self.client.generate_content_async(prompt, generation_config=self._get_generation_config(**kwargs))

    def _extract_usage(self, response) -> dict:
        """Extract token usage from Gemini's response."""
        # For new Gemini models, use the prompt and the generated text for token estimation
        try:
            text = response.candidates[0].content.parts[0].text
        except Exception:
            text = ""
        # We don't have prompt text in the response, so just estimate from the input prompt
        # This is a rough estimate, you may want to improve this if the SDK provides token counts
        prompt_tokens = 0  # Not available in response
        completion_tokens = len(text) // 4
        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens
        }

    def _format_response(self, response) -> LLMResponse:
        """Format Gemini's response into a standard format."""
        try:
            text = response.candidates[0].content.parts[0].text
        except Exception:
            text = ""
        return {
            "choices": [{
                "message": {
                    "content": text
                }
            }]
        }

    def _convert_messages_to_prompt(self, messages: list) -> str:
        """Convert OpenAI-style messages to Gemini prompt format."""
        prompt = ""
        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "system":
                prompt += f"System: {content}\n"
            elif role == "user":
                prompt += f"User: {content}\n"
            elif role == "assistant":
                prompt += f"Assistant: {content}\n"
        return prompt.strip()

    def _get_generation_config(self, **kwargs):
        """Get Gemini generation configuration."""
        return {
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 0.95),
            "top_k": kwargs.get("top_k", 40),
            "max_output_tokens": kwargs.get("max_tokens", 2048),
        }

    def _handle_error(self, error: Exception) -> None:
        """Handle Gemini-specific errors."""
        error_str = str(error).lower()
        if "quota" in error_str or "rate limit" in error_str:
            raise RateLimitError("Gemini rate limit exceeded")
        elif "api key" in error_str or "authentication" in error_str:
            raise AuthError("Gemini authentication failed")
        elif "invalid" in error_str or "bad request" in error_str:
            raise BadRequestError(f"Gemini invalid request: {error_str}")
        raise error 