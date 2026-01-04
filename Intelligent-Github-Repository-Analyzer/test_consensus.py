"""
Test script for consensus mechanism
"""

from questions import compute_consensus

# Test case 1: Three similar responses
print("=" * 80)
print("TEST 1: Three similar responses about Python")
print("=" * 80)

responses1 = [
    {"model_name": "Groq", "response": "This repository is a Python-based web application using Flask framework for backend development."},
    {"model_name": "HuggingFace", "response": "This is a Python web app built with Flask for the backend logic and routing."},
    {"model_name": "Gemini", "response": "The repository contains a Python Flask application that handles web requests."}
]

result1 = compute_consensus(responses1)
print(f"\nConsensus Response: {result1['consensus_response'][:100]}...")
print("\nModel Scores:")
for score in result1['model_scores']:
    print(f"  {score['model']:15} -> {score['avg_similarity']:.4f}")

# Test case 2: One outlier response
print("\n" + "=" * 80)
print("TEST 2: Two similar + one outlier")
print("=" * 80)

responses2 = [
    {"model_name": "Groq", "response": "This is a JavaScript React application for building user interfaces with component-based architecture."},
    {"model_name": "HuggingFace", "response": "The project is a React.js frontend application using modern JavaScript and JSX syntax."},
    {"model_name": "Gemini", "response": "This repository contains Java Spring Boot backend microservices."}  # Outlier
]

result2 = compute_consensus(responses2)
print(f"\nConsensus Response: {result2['consensus_response'][:100]}...")
print("\nModel Scores:")
for score in result2['model_scores']:
    print(f"  {score['model']:15} -> {score['avg_similarity']:.4f}")

# Test case 3: One error response
print("\n" + "=" * 80)
print("TEST 3: Two valid + one error")
print("=" * 80)

responses3 = [
    {"model_name": "Groq", "response": "This is a TypeScript Node.js application using Express framework."},
    {"model_name": "HuggingFace", "response": "Error getting response from HuggingFace: Timeout"},
    {"model_name": "Gemini", "response": "The repository is a Node.js backend built with Express and TypeScript."}
]

result3 = compute_consensus(responses3)
print(f"\nConsensus Response: {result3['consensus_response'][:100]}...")
print("\nModel Scores:")
for score in result3['model_scores']:
    print(f"  {score['model']:15} -> {score['avg_similarity']:.4f}")

print("\n" + "=" * 80)
print("ALL CONSENSUS TESTS COMPLETED")
print("=" * 80)
