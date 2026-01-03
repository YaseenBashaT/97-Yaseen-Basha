# 🧠 Smart Repository Analyzer (Multi-LLM Ready)

## 📌 Problem Statement
Single-LLM tools used for understanding large GitHub repositories often produce hallucinated or incomplete answers, making them unreliable for productivity-critical tasks like code understanding and architectural analysis.

## 💡 Solution
This project is an **AI-powered GitHub Repository Analyzer** designed to evolve into a **Multi-LLM Consensus Engine**.  
It analyzes repositories, retrieves relevant context, and answers user questions reliably by laying the foundation for multi-model agreement instead of single-model dependency.

---


## 🏗️ Architecture

```text
User Question
└── Repository Context Retrieval (BM25)
    └── LLM Processing (Groq / LLaMA)
        └── [Planned] Multi-LLM Consensus Layer
            └── Final Answer


```


---

## 🧠 AI & ML Concepts Used
- Large Language Models (LLMs)
- Prompt & Context Engineering
- BM25 Document Ranking
- Text Embeddings (planned)
- Multi-Model Consensus (planned)
- Foundations for Agentic AI & RAG

---

## 🔧 Tech Stack
- **Language:** Python 3.12
- **UI:** Streamlit
- **LLM Providers:**  
  - Groq API (LLaMA models)  
  - Hugging Face Inference API (Mistral
  - Gemini API
- **Framework:** LangChain
- **NLP:** NLTK
- **Ranking:** rank-bm25
- **Repo Handling:** GitPython
- **Visualization:** Plotly, NetworkX


---

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
python3 -c "import nltk; nltk.download('punkt_tab')"
export GROQ_API_KEY=your_key
python3 -m streamlit run main.py
```
App runs at: http://localhost:8501
🔁 Multi-LLM Consensus (Planned)

    Independent queries to multiple LLMs

    Response embeddings

    Cosine similarity scoring

    Final answer based on highest agreement


🤖 AI Tool Usage

    GitHub Copilot (code assistance)

    ChatGPT (design & architecture)

AI interaction logs are retained as per hackathon guidelines.
🏁 Conclusion

This project delivers a practical, extensible, and production-oriented AI system for repository understanding, with a clear roadmap toward reliable multi-model consensus-based reasoning.
