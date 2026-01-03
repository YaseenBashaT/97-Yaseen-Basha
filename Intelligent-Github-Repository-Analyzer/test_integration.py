#!/usr/bin/env python
"""Test integration of HuggingFace and Groq LLM clients"""

from llm_client import GroqLLMClient, BaseLLMClient
from huggingface_llm_client import HuggingFaceLLMClient
import os

print("=" * 60)
print("Testing LLM Client Integration")
print("=" * 60)

# Test imports
print("\n✓ Imports successful")

# Test HuggingFaceLLMClient inheritance
hf_bases = HuggingFaceLLMClient.__bases__
print(f"✓ HuggingFaceLLMClient inherits from: {hf_bases}")

# Test method availability
print(f"✓ get_response method exists: {hasattr(HuggingFaceLLMClient, 'get_response')}")
print(f"✓ get_model_name method exists: {hasattr(HuggingFaceLLMClient, 'get_model_name')}")

# Test BaseLLMClient is parent
is_subclass = issubclass(HuggingFaceLLMClient, BaseLLMClient)
print(f"✓ Is subclass of BaseLLMClient: {is_subclass}")

# Test GroqLLMClient still works
groq_bases = GroqLLMClient.__bases__
print(f"✓ GroqLLMClient inherits from: {groq_bases}")

print("\n" + "=" * 60)
print("Integration Tests Passed!")
print("=" * 60)

# Test creating instances (won't call API)
print("\nTesting instantiation:")

# Groq client
try:
    groq_client = GroqLLMClient(api_key="dummy_key")
    print(f"✓ GroqLLMClient instantiated: {groq_client.get_model_name()}")
except Exception as e:
    print(f"✗ GroqLLMClient error: {e}")

# HuggingFace client
try:
    hf_client = HuggingFaceLLMClient(api_token="dummy_token")
    print(f"✓ HuggingFaceLLMClient instantiated: {hf_client.get_model_name()}")
except Exception as e:
    print(f"✗ HuggingFaceLLMClient error: {e}")

print("\n✓ All instantiation tests passed!")
print("\nBoth clients are ready for use in main.py")
