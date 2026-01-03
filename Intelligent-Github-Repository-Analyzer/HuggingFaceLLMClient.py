import os
import requests
from base_llm_client import BaseLLMClient

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
            # Handle simple API errors (timeout / non-200 response)
            return f"Error: {str(e)}"
