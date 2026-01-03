"""
Abstract LLM Client Interface and Implementations

This module provides a pluggable interface for multiple LLM providers.
Currently implements Groq, but can be extended for other providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import time
import random
from groq import Groq
import os


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        """
        Get a response from the LLM given a prompt.
        
        Args:
            prompt: The input prompt
            
        Returns:
            The LLM's response as a string
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """
        Get the name/identifier of the model.
        
        Returns:
            Model name/identifier
        """
        pass


class GroqLLMClient(BaseLLMClient):
    """Groq API LLM Client Implementation"""
    
    def __init__(self, api_key: str = None, model_name: str = "llama-3.3-70b-versatile"):
        """
        Initialize Groq LLM Client
        
        Args:
            api_key: Groq API key. If None, reads from GROQ_API_KEY env var
            model_name: Model to use (default: llama-3.3-70b-versatile)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model_name = model_name
        self._client = Groq(api_key=self.api_key)
    
    def get_response(self, prompt: str) -> str:
        """
        Get response from Groq API with retry logic
        
        Args:
            prompt: The input prompt
            
        Returns:
            The LLM's response text
        """
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = self._client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that analyzes code repositories."},
                        {"role": "user", "content": prompt}
                    ],
                    timeout=30
                )
                return response.choices[0].message.content
                
            except Exception as e:
                error_message = str(e)
                
                # Handle specific error types
                if "503" in error_message or "Service unavailable" in error_message:
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2 ** attempt) + random.uniform(0, 1)
                        print(f"Groq service temporarily unavailable. Retrying in {wait_time:.1f} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RuntimeError("Groq service unavailable after retries")
                
                elif "rate limit" in error_message.lower():
                    if attempt < max_retries - 1:
                        wait_time = 60
                        print(f"Rate limit reached. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RuntimeError("Rate limit exceeded")
                
                else:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise
        
        raise RuntimeError("Failed to get response from Groq after retries")
    
    def get_model_name(self) -> str:
        """Return the model name"""
        return self.model_name
