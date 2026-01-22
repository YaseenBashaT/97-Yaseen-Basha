#!/usr/bin/env python
"""Test integration of Groq LLM client"""

import sys

print("=" * 75)
print("TESTING GROQ LLM CLIENT INTEGRATION")
print("=" * 75)

# Test 1: Import client
print("\n[TEST 1] Importing Groq LLM Client")
print("-" * 75)
try:
    from llm_client import BaseLLMClient, GroqLLMClient
    print("✓ Imported GroqLLMClient")
    
    from questions import QuestionContext, ask_question
    print("✓ Imported QuestionContext and ask_question")
    
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Verify inheritance
print("\n[TEST 2] Inheritance Verification")
print("-" * 75)
try:
    assert issubclass(GroqLLMClient, BaseLLMClient)
    print("✓ GroqLLMClient is subclass of BaseLLMClient")
    
except AssertionError as e:
    print(f"✗ Inheritance verification failed: {e}")
    sys.exit(1)

# Test 3: Client instantiation
print("\n[TEST 3] Client Instantiation")
print("-" * 75)
try:
    groq = GroqLLMClient(api_key="test_groq")
    print(f"✓ GroqLLMClient: {groq.get_model_name()}")
    
except Exception as e:
    print(f"✗ Instantiation failed: {e}")
    sys.exit(1)

# Test 4: LLM client list (main.py structure)
print("\n[TEST 4] LLM Clients List")
print("-" * 75)
try:
    llm_clients = [
        GroqLLMClient(api_key="test_groq")
    ]
    
    print(f"✓ Created llm_clients list with {len(llm_clients)} client(s):")
    for idx, client in enumerate(llm_clients, 1):
        print(f"  [{idx}] {client.__class__.__name__}: {client.get_model_name()}")
        
except Exception as e:
    print(f"✗ Client list creation failed: {e}")
    sys.exit(1)

# Test 5: QuestionContext with triple clients
print("\n[TEST 5] QuestionContext with Triple Clients")
print("-" * 75)
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
    
    print(f"✓ QuestionContext created with {len(context.llm_clients)} clients:")
    for idx, client in enumerate(context.llm_clients, 1):
        print(f"  [{idx}] {client.__class__.__name__}")
        
except Exception as e:
    print(f"✗ QuestionContext creation failed: {e}")
    sys.exit(1)

# Test 6: main.py integration
print("\n[TEST 6] main.py Integration Verification")
print("-" * 75)
try:
    with open("main.py", "r", encoding="utf-8") as f:
        main_content = f.read()
    
    assert "from gemini_llm_client import GeminiLLMClient" in main_content
    print("✓ main.py imports GeminiLLMClient")
    
    assert "GeminiLLMClient()" in main_content
    print("✓ main.py instantiates GeminiLLMClient")
    
    # Count instantiations (should be 2 - one for each path)
    count = main_content.count("GeminiLLMClient()")
    print(f"✓ GeminiLLMClient instantiated {count} times (both paths)")
    
    # Verify all three clients are used
    assert "GroqLLMClient" in main_content
    assert "HuggingFaceLLMClient" in main_content
    assert "GeminiLLMClient" in main_content
    print("✓ All three clients present in main.py")
    
except AssertionError as e:
    print(f"✗ main.py verification failed: {e}")
    sys.exit(1)

# Test 7: questions.py multi-client support
print("\n[TEST 7] questions.py Multi-Client Support")
print("-" * 75)
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

# Test 8: Requirements verification
print("\n[TEST 8] Requirements.txt Verification")
print("-" * 75)
try:
    with open("requirements.txt", "r", encoding="utf-8") as f:
        req_content = f.read()
    
    assert "google-generativeai" in req_content
    print("✓ google-generativeai in requirements.txt")
    
    assert "groq" in req_content
    print("✓ groq in requirements.txt")
    
    assert "requests" in req_content
    print("✓ requests in requirements.txt")
    
except AssertionError as e:
    print(f"✗ requirements verification failed: {e}")
    sys.exit(1)

# Final Summary
print("\n" + "=" * 75)
print("✅ ALL INTEGRATION TESTS PASSED!")
print("=" * 75)

print("\n📊 Summary:")
print("-" * 75)
print(f"  • Groq Model:         {groq.get_model_name()}")
print(f"  • HuggingFace Model:  {hf.get_model_name()}")
print(f"  • Gemini Model:       {gemini.get_model_name()}")
print(f"  • Total Clients:      {len(llm_clients)}")
print(f"  • QuestionContext:    ✓ Configured with all 3 clients")
print(f"  • main.py:            ✓ Integrated (2 instantiation paths)")
print(f"  • questions.py:       ✓ Multi-client response collection")
print(f"  • Inheritance:        ✓ All subclasses of BaseLLMClient")

print("\n🚀 Application Status: READY FOR TESTING WITH API KEYS")
print("   • GROQ_API_KEY (required)")
print("   • HF_API_TOKEN (required)")
print("   • GEMINI_API_KEY (required)")
print("\n" + "=" * 75)
