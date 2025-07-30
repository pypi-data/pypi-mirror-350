"""LLM provider clients."""

from abc import ABC, abstractmethod

from .config import LLMConfig, LLMProvider


class LLMClient(ABC):
    """Base class for LLM clients."""

    def __init__(self, config: LLMConfig):
        """Initialize the LLM client.

        Args:
            config: LLM configuration
        """
        self.config = config

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate text from a prompt.

        Args:
            prompt: The prompt to generate from

        Returns:
            Generated text
        """
        pass


class OpenAIClient(LLMClient):
    """OpenAI API client."""

    async def generate(self, prompt: str) -> str:
        """Generate text using OpenAI.

        Args:
            prompt: The prompt to generate from

        Returns:
            Generated text
        """
        try:
            # Only checking if importable
            __import__("openai")
        except ImportError as err:
            raise ImportError(
                "OpenAI support requires the openai package."
                "Install with 'pip install medium-converter[openai]'"
            ) from err

        # Placeholder for real implementation
        return f"Enhanced with OpenAI: {prompt[:50]}..."


class AnthropicClient(LLMClient):
    """Anthropic API client."""

    async def generate(self, prompt: str) -> str:
        """Generate text using Anthropic.

        Args:
            prompt: The prompt to generate from

        Returns:
            Generated text
        """
        try:
            # Only checking if importable
            __import__("anthropic")
        except ImportError as err:
            raise ImportError(
                "Anthropic support requires the anthropic package."
                "Install with 'pip install medium-converter[anthropic]'"
            ) from err

        # Placeholder for real implementation
        return f"Enhanced with Anthropic: {prompt[:50]}..."


class GoogleClient(LLMClient):
    """Google API client."""

    async def generate(self, prompt: str) -> str:
        """Generate text using Google.

        Args:
            prompt: The prompt to generate from

        Returns:
            Generated text
        """
        try:
            # Only checking if importable
            __import__("google.generativeai")
        except ImportError as err:
            raise ImportError(
                "Google support requires google-generativeai."
                "Install with 'pip install medium-converter[google]'"
            ) from err

        # Placeholder for real implementation
        return f"Enhanced with Google: {prompt[:50]}..."


class LiteLLMClient(LLMClient):
    """LiteLLM client for unified access to multiple providers."""

    async def generate(self, prompt: str) -> str:
        """Generate text using LiteLLM.

        Args:
            prompt: The prompt to generate from

        Returns:
            Generated text
        """
        try:
            # Only checking if importable
            __import__("litellm")
        except ImportError as err:
            raise ImportError(
                "LiteLLM support requires the litellm package."
                "Install with 'pip install medium-converter[llm]'"
            ) from err

        # Placeholder for real implementation
        return f"Enhanced with LiteLLM: {prompt[:50]}..."


def get_llm_client(config: LLMConfig) -> LLMClient:
    """Get an LLM client based on the provider.

    Args:
        config: LLM configuration

    Returns:
        LLM client
    """
    # Always use LiteLLM if available
    try:
        # We only need to check if litellm is importable
        __import__("litellm")
        return LiteLLMClient(config)
    except ImportError:
        pass

    # Fallback to specific providers
    if config.provider == LLMProvider.OPENAI:
        return OpenAIClient(config)
    elif config.provider == LLMProvider.ANTHROPIC:
        return AnthropicClient(config)
    elif config.provider == LLMProvider.GOOGLE:
        return GoogleClient(config)
    elif config.provider == LLMProvider.MISTRAL:
        # Placeholder for Mistral client
        return OpenAIClient(config)  # Temporary use OpenAI client
    elif config.provider == LLMProvider.LOCAL:
        # Placeholder for local client
        return OpenAIClient(config)  # Temporary use OpenAI client
    else:
        # Fallback to OpenAI
        return OpenAIClient(config)
