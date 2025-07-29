"""
Anthropic LLM provider implementation.
"""

import anthropic
from typing import Any
from .base import LLMBase

class AnthropicProvider(LLMBase):
    """Anthropic implementation of the LLM provider."""
    
    def __init__(self, api_key: str):
        """
        Initialize the Anthropic provider.
        
        Args:
            api_key: Anthropic API key
        """
        super().__init__(api_key)
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate_code(self, prompt: str) -> str:
        """
        Generate pandas code using Anthropic's API.
        
        Args:
            prompt: Natural language prompt
            
        Returns:
            Generated pandas code
        """
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.1,
            system="You are a pandas expert. Generate only the code, no explanations.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text.strip()
    
    def summarize(self, result: Any) -> str:
        """
        Generate a natural language summary using Anthropic's API.
        
        Args:
            result: The result to summarize
            
        Returns:
            Natural language summary
        """
        prompt = f"""Summarize this pandas operation result in natural language:

{result}

Summary:"""
        
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.3,
            system="You are a data analyst. Provide a clear, concise summary.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text.strip() 