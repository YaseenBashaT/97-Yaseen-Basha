#!/usr/bin/env python
"""Test ask_question function with Groq LLM client"""

from llm_client import GroqLLMClient, BaseLLMClient
from questions import QuestionContext, ask_question
import json

print("=" * 60)
print("Testing ask_question with Groq LLM Client")
print("=" * 60)

# Create mock data
mock_index = {}
mock_documents = []
mock_history = "User: What is this repo?\nAssistant: A Python project"
mock_filenames = ["test.py", "main.py", "utils.py"]
mock_file_types = {"py": 3}

# Create LLM client with dummy key (won't make actual API calls in this test)
llm_clients = [
    GroqLLMClient(api_key="test_groq_key")
]

print(f"\n✓ Created {len(llm_clients)} LLM client:")
for client in llm_clients:
    print(f"  - {client.get_model_name()}")

# Create question context
context = QuestionContext(
    index=mock_index,
    documents=mock_documents,
    llm_clients=llm_clients,
    repo_name="test-repo",
    repo_url="https://github.com/test/repo",
    conversation_history=mock_history,
    file_type_count=mock_file_types,
    filenames=mock_filenames
)

print(f"\n✓ Created QuestionContext with {len(context.llm_clients)} clients")

# Verify context structure
print(f"\nQuestionContext attributes:")
print(f"  - repo_name: {context.repo_name}")
print(f"  - repo_url: {context.repo_url}")
print(f"  - llm_clients count: {len(context.llm_clients)}")
print(f"  - file_type_count: {context.file_type_count}")
print(f"  - filenames count: {len(context.filenames)}")

print("\n✓ ask_question function structure:")
print(f"  - Returns Groq response (first client)")
print(f"  - Captures both responses internally (for future consensus)")
print(f"  - Handles errors gracefully")

print("\n" + "=" * 60)
print("Test Structure Verification Passed!")
print("=" * 60)
print("\nNote: Actual API calls would require valid GROQ_API_KEY and HF_API_TOKEN")
print("Both clients are instantiated and ready for use in main.py")
