"""
OpenAI LLM provider implementation.
"""

from openai import OpenAI
from typing import Any
from .base import LLMBase

class OpenAIProvider(LLMBase):
    """OpenAI implementation of the LLM provider."""
    
    def __init__(self, api_key: str):
        """
        Initialize the OpenAI provider.
        
        Args:
            api_key: OpenAI API key
        """
        super().__init__(api_key)
        self.client = OpenAI(api_key=api_key)
    
    def generate_code(self, prompt: str) -> str:
        """
        Generate pandas code using OpenAI's API.
        
        Args:
            prompt: Natural language prompt
            
        Returns:
            Generated pandas code
        """
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a pandas expert. Generate only the code, no explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content.strip()
    
    def summarize(self, result: Any) -> str:
        """
        Generate a natural language summary using OpenAI's API.
        
        Args:
            result: The result to summarize
            
        Returns:
            Natural language summary
        """
        prompt = f"""Summarize this pandas operation result in natural language:

{result}

Summary:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a data analyst. Provide a clear, concise summary."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip() 