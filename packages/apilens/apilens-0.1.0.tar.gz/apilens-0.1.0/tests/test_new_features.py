import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from apilens import OpenAIWrapper, AnthropicWrapper
from apilens.types import RateLimitError, AuthError, BadRequestError, LLMResponse

# Mock responses
MOCK_OPENAI_RESPONSE = Mock()
MOCK_OPENAI_RESPONSE.choices = [Mock(message=Mock(content="Hello!"))]
MOCK_OPENAI_RESPONSE.usage = Mock()
MOCK_OPENAI_RESPONSE.usage.prompt_tokens = 10
MOCK_OPENAI_RESPONSE.usage.completion_tokens = 20

MOCK_ANTHROPIC_RESPONSE = Mock()
MOCK_ANTHROPIC_RESPONSE.content = [Mock(text="Hello!")]
MOCK_ANTHROPIC_RESPONSE.usage = Mock()
MOCK_ANTHROPIC_RESPONSE.usage.input_tokens = 10
MOCK_ANTHROPIC_RESPONSE.usage.output_tokens = 20

@pytest.fixture
def openai_wrapper():
    with patch('apilens.openai_wrapper.OPENAI_API_KEY', 'fake-key'):
        return OpenAIWrapper(model="gpt-3.5-turbo")

@pytest.fixture
def anthropic_wrapper():
    with patch('apilens.anthropic_wrapper.ANTHROPIC_API_KEY', 'fake-key'):
        return AnthropicWrapper(model="claude-3-opus-20240229")

# Test Async Functionality
@pytest.mark.asyncio
async def test_async_chat_completion_openai(openai_wrapper):
    with patch.object(openai_wrapper, '_make_async_api_call', new=AsyncMock(return_value=MOCK_OPENAI_RESPONSE)):
        response = await openai_wrapper.async_chat_completion(
            messages=[{"role": "user", "content": "Hello!"}]
        )
        assert isinstance(response, dict)
        assert response["choices"][0]["message"]["content"] == "Hello!"
        assert "usage" in response
        assert "cost" in response

@pytest.mark.asyncio
async def test_async_chat_completion_anthropic(anthropic_wrapper):
    with patch.object(anthropic_wrapper, '_make_async_api_call', new=AsyncMock(return_value=MOCK_ANTHROPIC_RESPONSE)):
        response = await anthropic_wrapper.async_chat_completion(
            messages=[{"role": "user", "content": "Hello!"}]
        )
        assert isinstance(response, dict)
        assert response["choices"][0]["message"]["content"] == "Hello!"
        assert "usage" in response
        assert "cost" in response

# Test Streaming Functionality
def test_chat_completion_stream_openai(openai_wrapper):
    mock_stream = [
        MOCK_OPENAI_RESPONSE,
        MOCK_OPENAI_RESPONSE
    ]
    with patch.object(openai_wrapper, '_make_api_call', return_value=mock_stream):
        responses = list(openai_wrapper.chat_completion_stream(
            messages=[{"role": "user", "content": "Hello!"}]
        ))
        assert len(responses) == 2
        assert responses[0]["choices"][0]["message"]["content"] == "Hello!"
        assert responses[1]["choices"][0]["message"]["content"] == "Hello!"

# Test Error Handling
def test_rate_limit_error_openai(openai_wrapper):
    with patch.object(openai_wrapper, '_make_api_call', side_effect=RateLimitError("Rate limit exceeded")):
        with pytest.raises(RateLimitError):
            openai_wrapper.chat_completion(
                messages=[{"role": "user", "content": "Hello!"}]
            )

def test_auth_error_openai(openai_wrapper):
    with patch.object(openai_wrapper, '_make_api_call', side_effect=AuthError("Authentication failed")):
        with pytest.raises(AuthError):
            openai_wrapper.chat_completion(
                messages=[{"role": "user", "content": "Hello!"}]
            )

def test_bad_request_error_openai(openai_wrapper):
    with patch.object(openai_wrapper, '_make_api_call', side_effect=BadRequestError("Invalid request")):
        with pytest.raises(BadRequestError):
            openai_wrapper.chat_completion(
                messages=[{"role": "user", "content": "Hello!"}]
            )

# Test Retry Functionality
def test_retry_success_after_failure(openai_wrapper):
    call_count = {"count": 0}
    def flaky_call(*args, **kwargs):
        if call_count["count"] == 0:
            call_count["count"] += 1
            raise RateLimitError("Rate limit")
        return MOCK_OPENAI_RESPONSE
    with patch.object(openai_wrapper, '_make_api_call', side_effect=flaky_call):
        response = openai_wrapper.chat_completion(
            messages=[{"role": "user", "content": "Hello!"}]
        )
        assert response["choices"][0]["message"]["content"] == "Hello!"
        assert call_count["count"] == 1

def test_retry_exhaustion(openai_wrapper):
    with patch.object(openai_wrapper, '_make_api_call', side_effect=RateLimitError("Rate limit")):
        with pytest.raises(RateLimitError):
            openai_wrapper.chat_completion(
                messages=[{"role": "user", "content": "Hello!"}],
            )

# Test Custom Configuration
def test_custom_retry_config(openai_wrapper):
    wrapper = OpenAIWrapper(
        model="gpt-3.5-turbo",
        max_retries=5,
        backoff_base=2.0,
        timeout=60
    )
    assert wrapper.max_retries == 5
    assert wrapper.backoff_base == 2.0
    assert wrapper.timeout == 60

# Test Response Format
def test_response_format_openai(openai_wrapper):
    with patch.object(openai_wrapper, '_make_api_call', return_value=MOCK_OPENAI_RESPONSE):
        response = openai_wrapper.chat_completion(
            messages=[{"role": "user", "content": "Hello!"}]
        )
        assert isinstance(response, dict)
        assert "choices" in response
        assert "usage" in response
        assert "cost" in response
        assert isinstance(response["cost"], float)

def test_response_format_anthropic(anthropic_wrapper):
    with patch.object(anthropic_wrapper, '_make_api_call', return_value=MOCK_ANTHROPIC_RESPONSE):
        response = anthropic_wrapper.chat_completion(
            messages=[{"role": "user", "content": "Hello!"}]
        )
        assert isinstance(response, dict)
        assert "choices" in response
        assert "usage" in response
        assert "cost" in response
        assert isinstance(response["cost"], float) 