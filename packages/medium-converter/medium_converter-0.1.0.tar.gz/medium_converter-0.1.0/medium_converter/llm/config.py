"""LLM configuration for Medium Converter."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    MISTRAL = "mistral"
    LOCAL = "local"
    CUSTOM = "custom"


class LLMConfig(BaseModel):
    """Configuration for LLM integration."""

    provider: LLMProvider = LLMProvider.OPENAI
    model: str = "gpt-3.5-turbo"
    api_key: str | None = None
    temperature: float = 0.7
    max_tokens: int | None = None
    top_p: float = 1.0
    top_k: int | None = None
    stop_sequences: list[str] = Field(default_factory=list)
    timeout: int = 60
    extra_params: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_env(cls) -> "LLMConfig":
        """Create LLM config from environment variables.

        Returns:
            LLMConfig instance with values from environment
        """
        import os

        # Default to OpenAI if OPENAI_API_KEY is set
        if os.environ.get("OPENAI_API_KEY"):
            return cls(
                provider=LLMProvider.OPENAI,
                api_key=os.environ.get("OPENAI_API_KEY"),
                model=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo"),
            )

        # Check for Anthropic
        if os.environ.get("ANTHROPIC_API_KEY"):
            return cls(
                provider=LLMProvider.ANTHROPIC,
                api_key=os.environ.get("ANTHROPIC_API_KEY"),
                model=os.environ.get("ANTHROPIC_MODEL", "claude-3-sonnet-20240229"),
            )

        # Check for Google
        if os.environ.get("GOOGLE_API_KEY"):
            return cls(
                provider=LLMProvider.GOOGLE,
                api_key=os.environ.get("GOOGLE_API_KEY"),
                model=os.environ.get("GOOGLE_MODEL", "gemini-pro"),
            )

        # Check for Mistral
        if os.environ.get("MISTRAL_API_KEY"):
            return cls(
                provider=LLMProvider.MISTRAL,
                api_key=os.environ.get("MISTRAL_API_KEY"),
                model=os.environ.get("MISTRAL_MODEL", "mistral-medium"),
            )

        # Fallback to default
        return cls()
