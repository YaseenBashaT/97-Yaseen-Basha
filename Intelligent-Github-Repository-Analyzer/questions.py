
from utility import format_document
from repo_reader import search_documents
from typing import List, Dict, Any
from llm_client import BaseLLMClient
from langchain_core.prompts import PromptTemplate
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize embedding model globally (loaded once)
_embedding_model = None

def get_embedding_model():
    """Lazy load the sentence transformer model"""
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _embedding_model

def compute_consensus(responses: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Compute consensus response using sentence embeddings and cosine similarity.
    
    Args:
        responses: List of dicts with 'model_name' and 'response' keys
        
    Returns:
        Dict with 'consensus_response' and 'model_scores'
    """
    # Filter out error responses
    valid_responses = [r for r in responses if not r['response'].startswith('Error getting response')]
    
    if len(valid_responses) == 0:
        return {
            "consensus_response": "No valid responses received from LLM clients",
            "model_scores": []
        }
    
    if len(valid_responses) == 1:
        return {
            "consensus_response": valid_responses[0]['response'],
            "model_scores": [{"model": valid_responses[0]['model_name'], "avg_similarity": 1.0}]
        }
    
    # Get embedding model
    model = get_embedding_model()
    
    # Compute embeddings for all responses
    response_texts = [r['response'] for r in valid_responses]
    embeddings = model.encode(response_texts, convert_to_numpy=True)
    
    # Compute pairwise cosine similarity matrix
    similarity_matrix = cosine_similarity(embeddings)
    
    # Calculate average similarity score for each response (excluding self-similarity)
    avg_similarities = []
    for i in range(len(valid_responses)):
        # Get similarities with all other responses (exclude diagonal)
        other_similarities = [similarity_matrix[i][j] for j in range(len(valid_responses)) if i != j]
        avg_sim = np.mean(other_similarities) if other_similarities else 0.0
        avg_similarities.append(avg_sim)
    
    # Find the response with highest average similarity
    best_idx = np.argmax(avg_similarities)
    
    # Prepare model scores
    model_scores = [
        {
            "model": valid_responses[i]['model_name'],
            "avg_similarity": float(avg_similarities[i])
        }
        for i in range(len(valid_responses))
    ]
    
    # Sort by similarity score descending
    model_scores.sort(key=lambda x: x['avg_similarity'], reverse=True)
    
    return {
        "consensus_response": valid_responses[best_idx]['response'],
        "model_scores": model_scores
    }


class QuestionContext:
    def __init__(self, index, documents, llm_clients: List[BaseLLMClient], repo_name, repo_url, conversation_history, file_type_count, filenames):
        self.index = index
        self.documents = documents
        self.llm_clients = llm_clients  # List of LLM clients instead of single chain
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.conversation_history = conversation_history
        self.file_type_count = file_type_count
        self.filenames = filenames
        
def ask_question(question: str, context: QuestionContext) -> str:
    """
    Ask a question and get responses from all configured LLM clients.
    Returns the response in a structured format with model name and response.
    
    Args:
        question: The user's question
        context: QuestionContext with repository and LLM info
        
    Returns:
        A formatted string containing responses from all LLM clients
    """
    relevant_docs = search_documents(question, context.index, context.documents, n_results=5)
    numbered_document = format_document(relevant_docs)

    question_context = f"This question is about the github repo '{context.repo_name}' availabe at {context.repo_url}. The most relevant documents are:\n\n{numbered_document}"
    
    # Create the prompt template
    template = '''
You are an expert code analyst assistant. You have access to the repository content and our conversation history.

CONVERSATION HISTORY:
{conversation_history}

REPOSITORY: {repo_name}
URL: {repo_url}
FILE TYPES: {file_type_count}

RELEVANT DOCUMENTS:
{numbered_documents}

USER QUESTION: {question}

IMPORTANT INSTRUCTIONS:
- Base your answer ONLY on the documents provided above
- Only cite files that are explicitly shown in the RELEVANT DOCUMENTS section
- If a file (like README.md) is not in the documents above, do NOT mention it or claim information comes from it
- Be specific about which document number you're referencing when citing information
- If you don't have enough information in the provided documents, say so clearly
- Keep the answer terse and direct. No preamble, no meta-commentary, no restating the question. Start with the answer.

Please analyze the provided documents and conversation history to answer the question comprehensively. Cite specific files and code sections when relevant.'''

    prompt_template = PromptTemplate(
        template=template,
        input_variables=["repo_name", "repo_url", "conversation_history", "numbered_documents", "question", "file_type_count"]
    )
    
    # Format the prompt with context variables
    formatted_prompt = prompt_template.format(
        repo_name=context.repo_name,
        repo_url=context.repo_url,
        conversation_history=context.conversation_history,
        numbered_documents=numbered_document,
        question=question,
        file_type_count=str(context.file_type_count)
    )
    
    # Get responses from all LLM clients
    responses = []
    print("\n" + "="*80)
    print("LLM RESPONSES FROM ALL MODELS")
    print("="*80)
    for llm_client in context.llm_clients:
        try:
            response_text = llm_client.get_response(formatted_prompt)
            response_data = {
                "model_name": llm_client.get_model_name(),
                "response": response_text
            }
            responses.append(response_data)
            print(f"\n--- {llm_client.get_model_name()} ---")
            print(response_text)
            print("-" * 40)
        except Exception as e:
            response_data = {
                "model_name": llm_client.get_model_name(),
                "response": f"Error getting response from {llm_client.get_model_name()}: {str(e)}"
            }
            responses.append(response_data)
            print(f"\n--- {llm_client.get_model_name()} ---")
            print(f"ERROR: {str(e)}")
            print("-" * 40)
    
    print("\n" + "="*80)
    
    # Compute consensus from all responses
    if responses:
        consensus_result = compute_consensus(responses)
        print("CONSENSUS RESULT")
        print("="*80)
        print(f"Selected response from: {consensus_result['model_scores'][0]['model'] if consensus_result['model_scores'] else 'N/A'}")
        print(f"Model similarity scores: {consensus_result['model_scores']}")
        print("="*80 + "\n")
        # Return only the consensus response to UI
        return consensus_result["consensus_response"]
    else:
        return "No response received from any LLM client"