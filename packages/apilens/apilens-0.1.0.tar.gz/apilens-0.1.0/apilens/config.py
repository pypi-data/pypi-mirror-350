"""
Config for API Lens: loads environment and model pricing.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

DB_PATH = os.getenv("DB_PATH", "apilens.db")

# Pricing per 1K tokens (in USD)
PRICING = {
    # OpenAI Models
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
    
    # Anthropic Models
    "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
    "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
    
    # Gemini Models
    "gemini-pro": {"input": 0.00025, "output": 0.0005},
    "gemini-pro-vision": {"input": 0.00025, "output": 0.0005},
    "gemini-2.5-pro-preview-05-06": {"input": 0.00025, "output": 0.0005},
}
