# APILens

A Python wrapper for various AI language model APIs that provides consistent interface, logging, and cost tracking across different providers.

## Features

- Unified interface for multiple AI providers
- Automatic retry mechanism with exponential backoff
- Usage tracking and cost calculation
- SQLite-based logging system
- Support for both synchronous and asynchronous operations
- Streaming support

## Installation

```bash
pip install apilens
```

## Usage

```python
from apilens import BaseAIWrapper

# Initialize your provider wrapper
wrapper = YourProviderWrapper(
    provider_name="your_provider",
    model="your_model",
    user_id="optional_user_id",
    tenant_id="optional_tenant_id"
)

# Make a chat completion request
response = wrapper.chat_completion([
    {"role": "user", "content": "Hello, how are you?"}
])
```

## License

MIT License
