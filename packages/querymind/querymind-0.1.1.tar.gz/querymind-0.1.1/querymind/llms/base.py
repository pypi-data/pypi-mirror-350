"""
Base class for LLM providers.
"""

from abc import ABC, abstractmethod
from typing import Optional

class LLMBase(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, api_key: str):
        """
        Initialize the LLM provider.
        
        Args:
            api_key: API key for the provider
        """
        self.api_key = api_key
    
    @abstractmethod
    def generate_code(self, prompt: str) -> str:
        """
        Generate pandas code from a natural language prompt.
        
        Args:
            prompt: Natural language prompt describing the desired pandas operation
            
        Returns:
            Generated pandas code as a string
        """
        pass
    
    @abstractmethod
    def summarize(self, result: any) -> str:
        """
        Generate a natural language summary of the pandas operation result.
        
        Args:
            result: The result of the pandas operation
            
        Returns:
            Natural language summary of the result
        """
        pass 