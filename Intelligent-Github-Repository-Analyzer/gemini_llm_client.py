"""
Google Gemini API LLM Client Implementation

This module provides a Gemini LLM client using Google's Generative AI API.
"""

import os
import time
import random
from typing import Optional
import google.generativeai as genai
from llm_client import BaseLLMClient


class GeminiLLMClient(BaseLLMClient):
    """Google Gemini API LLM Client Implementation"""
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model_name: str = "gemini-1.5-flash"
    ):
        """
        Initialize Gemini LLM Client
        
        Args:
            api_key: Google Generative AI API key. If None, reads from GEMINI_API_KEY env var
            model_name: Model to use (default: gemini-1.5-flash)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY environment variable.")
        
        # Configure the Generative AI client
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
    
    def get_response(self, prompt: str) -> str:
        """
        Get response from Google Gemini API with retry logic
        
        Args:
            prompt: The input prompt
            
        Returns:
            The LLM's response text
            
        Raises:
            RuntimeError: If API calls fail after retries
        """
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=1000,
                        temperature=0.7,
                    ),
                    request_options={"timeout": 30}
                )
                
                # Check if response was generated successfully
                if response.text:
                    return response.text.strip()
                else:
                    # Handle empty or blocked responses
                    if response.prompt_feedback:
                        feedback = response.prompt_feedback
                        if feedback.block_reason:
                            raise RuntimeError(f"Content blocked: {feedback.block_reason}")
                    raise RuntimeError("Empty response from Gemini API")
                    
            except (TimeoutError, TimeoutException) as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    print(f"Gemini request timeout. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise RuntimeError(f"Gemini request timeout after retries: {str(e)}")
            
            except genai.types.GoogleAPICallError as e:
                error_str = str(e)
                
                # Handle rate limiting (429 Too Many Requests)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    if attempt < max_retries - 1:
                        wait_time = 60
                        print(f"Gemini rate limit reached. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RuntimeError("Gemini rate limit exceeded after retries")
                
                # Handle service unavailable (503)
                elif "503" in error_str or "SERVICE_UNAVAILABLE" in error_str:
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2 ** attempt) + random.uniform(0, 1)
                        print(f"Gemini service unavailable. Retrying in {wait_time:.1f} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RuntimeError("Gemini service unavailable after retries")
                
                else:
                    if attempt < max_retries - 1:
                        wait_time = retry_delay
                        print(f"Gemini API error: {error_str}. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RuntimeError(f"Gemini API error: {error_str}")
            
            except Exception as e:
                error_str = str(e)
                
                # Handle connection errors
                if "connection" in error_str.lower() or "network" in error_str.lower():
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2 ** attempt)
                        print(f"Connection error to Gemini. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RuntimeError(f"Connection error to Gemini after retries: {error_str}")
                
                # Generic error handling
                if attempt < max_retries - 1:
                    wait_time = retry_delay
                    print(f"Gemini error: {error_str}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise RuntimeError(f"Gemini API error after retries: {error_str}")
        
        raise RuntimeError("Failed to get response from Gemini after retries")
    
    def get_model_name(self) -> str:
        """Return the model name/identifier"""
        return self.model_name


# Handle potential import issues
try:
    from google.api_core.exceptions import InvalidArgument as TimeoutException
except ImportError:
    TimeoutException = TimeoutError
