from abc import ABC, abstractmethod
import time
import asyncio
from typing import Optional, Dict, Any, Iterator, AsyncIterator, List, Callable, TypeVar, Union
from .logger import _APILogger
from .types import LLMResponse, APILensError, RateLimitError, AuthError, BadRequestError
from .config import PRICING
import logging
import sqlite3

logger = logging.getLogger(__name__)

T = TypeVar('T')

class BaseAIWrapper(ABC):
    """
    Base class for all AI provider wrappers.
    Handles common functionality like retries, logging, and cost calculation.
    """
    def __init__(
        self, 
        provider_name: str, 
        model: str, 
        db_path: str = "apilens.db", 
        user_id: Optional[str] = None, 
        tenant_id: Optional[str] = None,
        max_retries: int = 3,
        backoff_base: float = 2.0,
        timeout: int = 30,
        logger: Optional[_APILogger] = None,
        **kwargs
    ):
        self.provider_name = provider_name
        self.model = model
        self._logger = logger or _APILogger(db_path)
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.timeout = timeout
        self.provider_config = kwargs
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database for logging."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS api_calls
            (timestamp TEXT, provider TEXT, model TEXT, prompt_tokens INTEGER,
             completion_tokens INTEGER, cost REAL, user_id TEXT, tenant_id TEXT)
        ''')
        conn.commit()
        conn.close()

    def _log_usage(self, prompt_tokens: int, completion_tokens: int, cost: float):
        """Log API usage to SQLite database."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO api_calls
            (timestamp, provider, model, prompt_tokens, completion_tokens, cost, user_id, tenant_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (time.strftime('%Y-%m-%d %H:%M:%S'), self.provider_name, self.model,
              prompt_tokens, completion_tokens, cost, self.user_id, self.tenant_id))
        conn.commit()
        conn.close()

    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost based on token usage."""
        pricing = PRICING.get(model, {"input": 0.03, "output": 0.06})
        return (prompt_tokens / 1000 * pricing["input"]) + (completion_tokens / 1000 * pricing["output"])

    @abstractmethod
    def _make_api_call(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """Make the actual API call to the provider."""
        pass

    @abstractmethod
    async def _make_async_api_call(self, messages: List[Dict[str, str]], **kwargs) -> Any:
        """Make an async API call to the provider."""
        pass

    @abstractmethod
    def _extract_usage(self, response: Any) -> Dict[str, int]:
        """Extract token usage from the provider's response."""
        pass

    @abstractmethod
    def _format_response(self, response: Any) -> LLMResponse:
        """Format the provider's response into a standard format."""
        pass

    def _retry_with_backoff(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Retry a function with exponential backoff."""
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except RateLimitError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    sleep_time = self.backoff_base ** attempt
                    logger.warning(f"Rate limit hit, retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    logger.error("Max retries exceeded")
                    raise
            except Exception as e:
                last_exception = e
                raise
        raise last_exception

    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """
        Make a chat completion request with retries and logging.
        This method now handles all business logic, including calling _make_api_call,
        _extract_usage, and _format_response.
        """
        # Input validation
        for i, msg in enumerate(messages):
            if not isinstance(msg, dict):
                raise ValueError(f"Message #{i} must be a dict, got {type(msg)}")
            if "role" not in msg:
                raise ValueError(f"Message #{i} missing 'role'")
            if "content" not in msg or not msg["content"]:
                raise ValueError(f"Message #{i} missing or empty 'content'")
        try:
            response = self._retry_with_backoff(self._make_api_call, messages, **kwargs)
            usage = self._extract_usage(response)
            cost = self._calculate_cost(self.model, usage["prompt_tokens"], usage["completion_tokens"])
            formatted = self._format_response(response)
            formatted["usage"] = usage
            formatted["cost"] = cost
            self._log_usage(usage["prompt_tokens"], usage["completion_tokens"], cost)
            return formatted
        except Exception as e:
            logger.error(f"Error in chat_completion: {e}")
            raise

    async def async_chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """
        Async version of chat_completion.
        """
        try:
            response = await self._make_async_api_call(messages, **kwargs)
            usage = self._extract_usage(response)
            cost = self._calculate_cost(self.model, usage["prompt_tokens"], usage["completion_tokens"])
            formatted = self._format_response(response)
            formatted["usage"] = usage
            formatted["cost"] = cost
            self._log_usage(usage["prompt_tokens"], usage["completion_tokens"], cost)
            return formatted
        except Exception as e:
            logger.error(f"Error in async_chat_completion: {e}")
            raise

    def chat_completion_stream(self, messages: List[Dict[str, str]], **kwargs) -> LLMResponse:
        """
        Stream chat completion responses.
        """
        try:
            for chunk in self._make_api_call(messages, stream=True, **kwargs):
                yield self._format_response(chunk)
        except Exception as e:
            logger.error(f"Error in chat_completion_stream: {e}")
            raise

    def log_call(
        self, 
        call_id: Optional[int] = None, 
        prompt_tokens: int = 0, 
        completion_tokens: int = 0, 
        cost: float = 0.0, 
        status: str = "pending", 
        error_message: Optional[str] = None
    ) -> int:
        """Log the API call with standardized format."""
        return self._logger.log_call(
            call_id=call_id,
            provider=self.provider_name,
            model=self.model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=cost,
            status=status,
            error_message=error_message,
            user_id=self.user_id,
            tenant_id=self.tenant_id
        ) 