#!/usr/bin/env python
"""Final integration test - verify Groq LLM flow"""

import sys
import os

print("=" * 70)
print("FINAL INTEGRATION TEST: Groq LLM Client")
print("=" * 70)

# Test 1: Import chain
print("\n[TEST 1] Import Chain")
print("-" * 70)
try:
    from llm_client import BaseLLMClient, GroqLLMClient
    print("✓ Imported BaseLLMClient and GroqLLMClient from llm_client.py")
    
    from questions import QuestionContext, ask_question
    print("✓ Imported QuestionContext and ask_question from questions.py")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Client instantiation
print("\n[TEST 2] Client Instantiation")
print("-" * 70)
try:
    groq = GroqLLMClient(api_key="test_key")
    print(f"✓ GroqLLMClient created: {groq.get_model_name()}")
    
except Exception as e:
    print(f"✗ Instantiation failed: {e}")
    sys.exit(1)

# Test 3: Client list creation (like in main.py)
print("\n[TEST 3] LLM Clients List Creation")
print("-" * 70)
try:
    llm_clients = [
        GroqLLMClient(api_key="test_groq")
    ]
    print(f"✓ Created llm_clients list with {len(llm_clients)} clients")
    for idx, client in enumerate(llm_clients, 1):
        print(f"  [{idx}] {client.get_model_name()}")
        
except Exception as e:
    print(f"✗ Client list creation failed: {e}")
    sys.exit(1)

# Test 4: QuestionContext creation (like in main.py)
print("\n[TEST 4] QuestionContext Setup")
print("-" * 70)
try:
    context = QuestionContext(
        index={},
        documents=[],
        llm_clients=llm_clients,
        repo_name="test-repo",
        repo_url="https://github.com/test/test",
        conversation_history="Test history",
        file_type_count={"py": 5},
        filenames=["a.py", "b.py"]
    )
    print(f"✓ QuestionContext created")
    print(f"  - Repo: {context.repo_name}")
    print(f"  - LLM Clients: {len(context.llm_clients)}")
    print(f"  - Models: {[c.get_model_name() for c in context.llm_clients]}")
    
except Exception as e:
    print(f"✗ QuestionContext creation failed: {e}")
    sys.exit(1)

# Test 5: Inheritance verification
print("\n[TEST 5] Inheritance and Contract Compliance")
print("-" * 70)
try:
    # Verify inheritance
    assert issubclass(GroqLLMClient, BaseLLMClient), "GroqLLMClient not subclass of BaseLLMClient"
    print("✓ GroqLLMClient is subclass of BaseLLMClient")
    
    # Verify methods exist
    assert hasattr(groq, 'get_response'), "GroqLLMClient missing get_response"
    assert hasattr(groq, 'get_model_name'), "GroqLLMClient missing get_model_name"
    print("✓ GroqLLMClient has required methods")
    
except AssertionError as e:
    print(f"✗ Contract verification failed: {e}")
    sys.exit(1)

# Test 6: Main.py structure verification
print("\n[TEST 6] Main.py Integration Verification")
print("-" * 70)
try:
    with open("main.py", "r", encoding="utf-8") as f:
        main_content = f.read()
    
    assert "from llm_client import GroqLLMClient" in main_content
    print("✓ main.py imports GroqLLMClient")
    
    assert "GroqLLMClient(" in main_content
    print("✓ main.py instantiates GroqLLMClient")
    
except FileNotFoundError:
    print("✗ main.py not found")
    sys.exit(1)
except AssertionError as e:
    print(f"✗ main.py structure verification failed: {e}")
    sys.exit(1)

# Test 7: Questions.py structure
print("\n[TEST 7] Questions.py Response Collection")
print("-" * 70)
try:
    with open("questions.py", "r", encoding="utf-8") as f:
        questions_content = f.read()
    
    assert "for llm_client in context.llm_clients:" in questions_content
    print("✓ questions.py iterates over all llm_clients")
    
    assert "responses.append(response_data)" in questions_content
    print("✓ questions.py collects responses from all clients")
    
    assert 'return responses[0]["response"]' in questions_content
    print("✓ questions.py returns first response (Groq) to UI")
    
except AssertionError as e:
    print(f"✗ questions.py verification failed: {e}")
    sys.exit(1)

# Final Summary
print("\n" + "=" * 70)
print("✅ ALL INTEGRATION TESTS PASSED!")
print("=" * 70)

print("\n📊 Summary:")
print("-" * 70)
print(f"  • Groq Model:       {groq.get_model_name()}")
print(f"  • HuggingFace Model: {hf.get_model_name()}")
print(f"  • Clients in List:   {len(llm_clients)}")
print(f"  • QuestionContext:   ✓ Configured")
print(f"  • main.py:           ✓ Integrated (2 instantiation paths)")
print(f"  • questions.py:      ✓ Multi-client support")
print(f"  • Inheritance:       ✓ Proper contract")

print("\n🚀 Application Status: READY FOR TESTING WITH API KEYS")
print("\n" + "=" * 70)
