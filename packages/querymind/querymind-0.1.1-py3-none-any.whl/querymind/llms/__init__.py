"""
LLM provider implementations and factory function.
"""

from .base import LLMBase
from .openai_llm import OpenAIProvider
from .anthropic_llm import AnthropicProvider

def get_llm(provider_name: str, api_key: str) -> LLMBase:
    """
    Factory function to get the appropriate LLM provider.
    
    Args:
        provider_name: Name of the LLM provider ("openai" or "anthropic")
        api_key: API key for the provider
        
    Returns:
        An instance of the requested LLM provider
        
    Raises:
        ValueError: If the provider is not supported
    """
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider
    }
    
    if provider_name not in providers:
        raise ValueError(f"Unsupported LLM provider: {provider_name}. "
                        f"Supported providers are: {list(providers.keys())}")
    
    return providers[provider_name](api_key)

__all__ = ["LLMBase", "OpenAIProvider", "AnthropicProvider", "get_llm"] 