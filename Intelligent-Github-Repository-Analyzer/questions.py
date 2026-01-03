
from utility import format_document
from repo_reader import search_documents
from typing import List, Dict, Any
from llm_client import BaseLLMClient
from langchain_core.prompts import PromptTemplate

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
    for llm_client in context.llm_clients:
        try:
            response_text = llm_client.get_response(formatted_prompt)
            response_data = {
                "model_name": llm_client.get_model_name(),
                "response": response_text
            }
            responses.append(response_data)
        except Exception as e:
            response_data = {
                "model_name": llm_client.get_model_name(),
                "response": f"Error getting response from {llm_client.get_model_name()}: {str(e)}"
            }
            responses.append(response_data)
    
    # For now, return only the first response text (single LLM mode)
    # Future: consensus logic will use all responses
    if responses:
        return responses[0]["response"]
    else:
        return "No response received from any LLM client"