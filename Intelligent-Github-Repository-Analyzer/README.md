# 🚀 AI-Powered GitHub Repository Analyzer (Multi-LLM Consensus Engine)

## 📌 Problem Statement
Developers and teams often need deep insights into unfamiliar codebases, but traditional search and keyword-based approaches are limited. Single-LLM tools are prone to hallucinations, lack consistency, and can miss important context. This makes them unreliable for productivity-critical tasks like code understanding, architectural analysis, and actionable recommendations.

---

## 💡 Solution Overview
This project delivers an **AI-powered GitHub Repository Analyzer** that:
- Clones and indexes public GitHub repositories
- Retrieves relevant content using lexical and semantic search
- Queries **multiple Large Language Models (LLMs)** in parallel
- Uses **semantic consensus logic** to produce the most reliable answer

By using multiple independent LLM providers and selecting the response with the highest semantic agreement, the system significantly reduces hallucination and improves answer reliability.

---

## 🏗️ Architecture

```text
User Question
└── Repository Context Retrieval (BM25)
    └── Multi-LLM Inference
        ├── Groq (LLaMA)
        ├── Hugging Face (Mistral)
        └── Gemini (gemini-1.5-flash)
            ↓
    Response Embeddings (all-MiniLM-L6-v2)
            ↓
    Cosine Similarity Consensus
            ↓
        Final Answer to UI

🧠 Key Features
✨ Core Capabilities

    Repository Cloning: Clone public GitHub repos from URL

    Indexing and Tokenization: Process files for efficient retrieval

    Document Ranking: BM25-based relevance ranking

    Multi-LLM Parallel Querying: Groq, Mistral and Gemini

    Consensus Logic: Embedding-based agreement selection

    Error Handling & Robustness: Timeouts, retries, failover

    Streamlit UI: Interactive, clean interface for questions

🔧 Technology Stack

    Language: Python 3.12

    Frontend: Streamlit (web UI)

    LLM Providers:

        Groq API (LLaMA models)

        Hugging Face Inference API (Mistral)

        Gemini API (gemini-1.5-flash)

    Vector/Embedding Support: sentence-transformers

    Retrieval: rank-bm25

    NLP: NLTK

    Repository Handling: GitPython

    Visualizations: Plotly, NetworkX

    Framework: LangChain

🚀 Getting Started
🛠 Prerequisites

    Python 3.12

    Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

📦 Install Dependencies

pip install -r requirements.txt

🧠 Download NLP Models

python3 -c "import nltk; nltk.download('punkt_tab')"

🔑 Set Environment Variables

Create a .env file and add:

GROQ_API_KEY=your_groq_api_key
HF_API_TOKEN=your_huggingface_token
GEMINI_API_KEY=your_gemini_api_key

▶️ Running the Application

python3 -m streamlit run main.py

Access the UI at:

http://localhost:8501

🔍 Usage Walkthrough

    Enter GitHub Repository URL
    Paste any public GitHub URL in the input box.

    Ask Questions
    Enter natural language questions about the repository’s code and structure.

    View Results
    Get the best consensus answer distilled from multiple LLMs.

📊 Consensus Mechanism

This system does not rely on a single LLM. Instead:

    Each model produces its own answer.

    Each answer is embedded using a shared embedding model.

    Cosine similarity is computed between all pairs.

    The response with the highest average agreement is selected.

This ensures:

    Suppression of hallucinated answers

    Better reliability across diverse contexts

    Stronger, consensus-guided answers

🧪 Evaluation Strategy

Evaluation is based on:

    Semantic agreement score

    Human qualitative validation

    Robustness against single-model failures

📜 Assumptions

    Only public GitHub repositories are supported

    Internet access required for external APIs

    Users supply valid API keys

🛡️ Guardrails

    Independent model execution with failover

    Timeout and retry logic

    Input sanitization and validation

    No API keys committed to source control

🪪 Tests

    test_cache.py: Verifies repository caching

    test_consensus.py: Verifies consensus logic correctness

    test_groq.py: Ensures Groq LLM integration

🤖 AI Tool Usage

    ChatGPT: Architecture design, planning, prompt guidance, review

    GitHub Copilot: Assisted code implementation under developer supervision

🏁 Conclusion

This repository is a robust, extensible, and evaluation-ready AI system that combines retrieval, multi-model inference, and semantic consensus to produce reliable answers about GitHub repositories. It demonstrates practical AI engineering beyond single-model approaches and aligns with real-world productivity and software engineering needs.
