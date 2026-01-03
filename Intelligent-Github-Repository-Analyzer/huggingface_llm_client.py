"""
Hugging Face Inference API LLM Client Implementation

This module provides a Hugging Face LLM client using the Inference API
with Mistral-7B-Instruct model.
"""

import os
import requests
import time
import random
from typing import Optional
from llm_client import BaseLLMClient


class HuggingFaceLLMClient(BaseLLMClient):
    def __init__(self):
        self.api_token = os.getenv("HF_API_TOKEN")
        self.model = "mistralai/Mistral-7B-Instruct-v0.2"
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"

    def get_response(self, prompt):
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {"inputs": prompt}
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()[0]['generated_text']  # Return plain text
        except requests.exceptions.RequestException as e:
            # Handle simple API errors
            return f"Error: {str(e)}"
    """Hugging Face Inference API LLM Client Implementation"""
    
    def __init__(
        self, 
        api_token: Optional[str] = None, 
        model_name: str = "mistralai/Mistral-7B-Instruct-v0.2"
    ):
        """
        Initialize Hugging Face LLM Client
        
        Args:
            api_token: Hugging Face API token. If None, reads from HF_API_TOKEN env var
            model_name: Model to use (default: mistralai/Mistral-7B-Instruct-v0.2)
        """
        self.api_token = api_token or os.getenv("HF_API_TOKEN")
        self.model_name = model_name
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        
        if not self.api_token:
            raise ValueError("Hugging Face API token not found. Set HF_API_TOKEN environment variable.")
    
    def get_response(self, prompt: str) -> str:
        """
        Get response from Hugging Face Inference API with retry logic
        
        Args:
            prompt: The input prompt
            
        Returns:
            The LLM's response text
            
        Raises:
            RuntimeError: If API calls fail after retries
        """
        max_retries = 3
        retry_delay = 1
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 1000,
                "temperature": 0.7,
                "top_p": 0.95
            }
        }
        
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                # Handle non-200 responses
                if response.status_code != 200:
                    error_text = response.text
                    
                    # Handle model loading (503 Temporarily Unavailable)
                    if response.status_code == 503:
                        if attempt < max_retries - 1:
                            wait_time = retry_delay * (2 ** attempt) + random.uniform(0, 1)
                            print(f"Hugging Face model loading. Retrying in {wait_time:.1f} seconds...")
                            time.sleep(wait_time)
                            continue
                        else:
                            raise RuntimeError("Hugging Face model unavailable after retries")
                    
                    # Handle rate limiting (429 Too Many Requests)
                    elif response.status_code == 429:
                        if attempt < max_retries - 1:
                            wait_time = 60
                            print(f"Hugging Face rate limit reached. Waiting {wait_time} seconds...")
                            time.sleep(wait_time)
                            continue
                        else:
                            raise RuntimeError("Hugging Face rate limit exceeded after retries")
                    
                    else:
                        raise RuntimeError(f"Hugging Face API error {response.status_code}: {error_text}")
                
                # Parse successful response
                response_data = response.json()
                
                # Handle both single response and list response formats
                if isinstance(response_data, list) and len(response_data) > 0:
                    if "generated_text" in response_data[0]:
                        # Extract generated text and remove the original prompt
                        generated = response_data[0]["generated_text"]
                        # The API returns the full text including prompt, so we extract just the new part
                        if prompt in generated:
                            return generated.replace(prompt, "", 1).strip()
                        return generated.strip()
                    else:
                        raise RuntimeError(f"Unexpected response format: {response_data}")
                elif isinstance(response_data, dict):
                    if "generated_text" in response_data:
                        generated = response_data["generated_text"]
                        if prompt in generated:
                            return generated.replace(prompt, "", 1).strip()
                        return generated.strip()
                    else:
                        raise RuntimeError(f"Unexpected response format: {response_data}")
                else:
                    raise RuntimeError(f"Unexpected response format: {response_data}")
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    print(f"Hugging Face request timeout. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise RuntimeError("Hugging Face request timeout after retries")
            
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    print(f"Connection error to Hugging Face. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise RuntimeError(f"Connection error to Hugging Face after retries: {str(e)}")
        
        raise RuntimeError("Failed to get response from Hugging Face after retries")
    
    def get_model_name(self) -> str:
        """Return the model name/identifier"""
        return self.model_name
