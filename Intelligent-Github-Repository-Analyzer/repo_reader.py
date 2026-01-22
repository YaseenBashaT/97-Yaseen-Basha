import os
import subprocess
import uuid
import numpy as np
from rank_bm25 import BM25Okapi
from langchain_community.document_loaders import DirectoryLoader, NotebookLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utility import clean_and_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

CHROMA_DB_DIR = "./chroma_db"
_retrieval_embedder = None
_chroma_client = None


def get_retrieval_embedder():
    """Lazy-load embedding model for retrieval."""
    global _retrieval_embedder
    if _retrieval_embedder is None:
        _retrieval_embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _retrieval_embedder


def get_chroma_client():
    """Lazy-load Chroma client with persistent local storage."""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.Client(Settings(persist_directory=CHROMA_DB_DIR, is_persistent=True))
    return _chroma_client

def clone_git_repo(url, path):
    """Clone a git repository with URL validation and auto-correction."""
    try:
        # Ensure URL has proper protocol
        if url.startswith('github.com/') or (not url.startswith('http://') and not url.startswith('https://') and not url.startswith('git@')):
            url = f'https://{url}'
        
        # Ensure URL ends with .git for consistency
        if not url.endswith('.git'):
            url = f'{url}.git'
        
        subprocess.run(['git', 'clone', url, path], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as ex:
        print(f"failed to clone repo: {ex}")
        # Try without .git suffix if it failed
        if url.endswith('.git'):
            try:
                url_without_git = url[:-4]
                subprocess.run(['git', 'clone', url_without_git, path], check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        return False
    
def load_and_index_files(repo_path):
    import glob as glob_module
    from langchain_core.documents import Document
    
    # Define file extensions we want to process
    extensions = ['txt', 'md', 'markdown', 'rst', 'py', 'js', 'ts', 'jsx', 'tsx', 'java', 'c', 'cpp', 'cs', 'go', 'rb', 'php', 'scala', 'html', 'htm', 'xml', 'json', 'yaml', 'yml', 'ini', 'toml', 'cfg', 'conf', 'sh', 'bash', 'css', 'scss', 'sql', 'vue', 'svelte', 'r', 'R', 'dart', 'kt', 'swift', 'pl', 'lua']
    
    file_type_counts = {}
    documents_dict = {}
    total_processed = 0
    total_errors = 0
    
    def load_file_content(file_path):
        """Load content from a single file with robust error handling"""
        try:
            # Skip very large files
            if os.path.getsize(file_path) > 10 * 1024 * 1024:  # 10MB limit
                return None
            
            # Try different encodings
            encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
            content = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                        content = f.read()
                    break
                except (UnicodeDecodeError, UnicodeError, PermissionError):
                    continue
                except Exception:
                    continue
            
            if content is None:
                return None
            
            # Skip empty or very short files
            if len(content.strip()) < 5:
                return None
            
            # Basic binary detection - skip files with too many null bytes or non-printable chars
            if '\x00' in content[:1000] or content.count('\x00') > 10:
                return None
            
            # Check if file appears to be text (reasonable ratio of printable characters)
            sample = content[:2000]  # Check first 2KB
            if sample:
                printable_count = sum(1 for c in sample if c.isprintable() or c in '\n\r\t')
                if printable_count / len(sample) < 0.7:  # Less than 70% printable = likely binary
                    return None
            
            return content
            
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return None
    
    # Process each file extension
    for ext in extensions:
        ext_file_count = 0
        
        # Find all files with this extension
        pattern = os.path.join(repo_path, '**', f'*.{ext}')
        matching_files = glob_module.glob(pattern, recursive=True)
        
        for file_path in matching_files:
            try:
                # Skip hidden files and directories
                if any(part.startswith('.') for part in os.path.relpath(file_path, repo_path).split(os.sep)):
                    if not any(file_path.endswith(f'.{allowed}') for allowed in ['gitignore', 'dockerignore', 'editorconfig']):
                        continue
                
                # Load file content
                content = load_file_content(file_path)
                if content is not None:
                    # Create document
                    relative_path = os.path.relpath(file_path, repo_path)
                    file_id = str(uuid.uuid4())
                    
                    doc = Document(
                        page_content=content,
                        metadata={
                            "source": relative_path,
                            "file_id": file_id
                        }
                    )
                    
                    documents_dict[file_id] = doc
                    ext_file_count += 1
                    total_processed += 1
                else:
                    total_errors += 1
                    
            except Exception as e:
                total_errors += 1
                continue
        
        if ext_file_count > 0:
            file_type_counts[ext] = ext_file_count
    
    print(f"Repository indexing complete: {total_processed} files processed, {total_errors} errors")
    print(f"File types found: {list(file_type_counts.keys())}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)

    split_documents = []
    for file_id, original_doc in documents_dict.items():
        split_docs = text_splitter.split_documents([original_doc])
        for i, split_doc in enumerate(split_docs):
            # Create unique chunk_id for each split document
            split_doc.metadata['chunk_id'] = f"{original_doc.metadata['file_id']}_chunk_{i}"
            split_doc.metadata['file_id'] = original_doc.metadata['file_id']
            split_doc.metadata['source'] = original_doc.metadata['source']

        split_documents.extend(split_docs)

    index = None
    chroma_collection = None
    collection_name = None

    if split_documents:
        # BM25 (lexical) index
        tokenized_documents = [clean_and_tokenize(doc.page_content) for doc in split_documents]
        index = BM25Okapi(tokenized_documents)

        # Dense embeddings stored in persistent ChromaDB (local disk)
        embedder = get_retrieval_embedder()
        embeddings = embedder.encode([doc.page_content for doc in split_documents], show_progress_bar=False)
        embeddings = np.asarray(embeddings, dtype=np.float32)

        client = get_chroma_client()
        collection_name = f"repo-{uuid.uuid4()}"
        # Recreate collection fresh to avoid stale data
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass
        chroma_collection = client.get_or_create_collection(name=collection_name, metadata={"source": "local"})

        chroma_collection.add(
            ids=[doc.metadata['chunk_id'] for doc in split_documents],
            documents=[doc.page_content for doc in split_documents],
            embeddings=embeddings.tolist(),
            metadatas=[{"source": doc.metadata.get("source", ""), "file_id": doc.metadata.get("file_id", ""), "chunk_id": doc.metadata.get("chunk_id", "")} for doc in split_documents]
        )

    return {
        "bm25": index,
        "chroma_collection": chroma_collection,
        "chroma_collection_name": collection_name
    }, split_documents, file_type_counts, [doc.metadata['source'] for doc in split_documents]

def search_documents(query, index_bundle, documents, n_results=5):
    """Hybrid search using BM25 + TF-IDF + Chroma (persistent local)."""
    if not documents:
        return []

    bm25_index = index_bundle.get("bm25") if isinstance(index_bundle, dict) else index_bundle
    chroma_collection = None
    if isinstance(index_bundle, dict):
        chroma_collection = index_bundle.get("chroma_collection")
        collection_name = index_bundle.get("chroma_collection_name")
        if chroma_collection is None and collection_name:
            client = get_chroma_client()
            try:
                chroma_collection = client.get_collection(name=collection_name)
                index_bundle["chroma_collection"] = chroma_collection
            except Exception:
                chroma_collection = None

    # BM25 lexical scores
    query_tokens = clean_and_tokenize(query)
    bm25_scores = bm25_index.get_scores(query_tokens) if bm25_index else np.zeros(len(documents))

    # TF-IDF semantic-lite scores
    tfidf_vectorizer = TfidfVectorizer(
        tokenizer=clean_and_tokenize,
        lowercase=True,
        stop_words='english',
        use_idf=True,
        smooth_idf=True,
        sublinear_tf=True,
    )
    tfidf_matrix = tfidf_vectorizer.fit_transform([doc.page_content for doc in documents])
    query_tfidf = tfidf_vectorizer.transform([query])
    cosine_sim_scores = cosine_similarity(query_tfidf, tfidf_matrix).flatten()

    # Chroma dense scores (convert distances to similarity)
    chroma_scores = np.zeros(len(documents))
    if chroma_collection is not None:
        try:
            embedder = get_retrieval_embedder()
            q_embed = embedder.encode([query], show_progress_bar=False)
            q_embed = np.asarray(q_embed, dtype=np.float32)
            result = chroma_collection.query(query_embeddings=q_embed.tolist(), n_results=min(n_results, len(documents)))
            if result and result.get("ids"):
                ids = result["ids"][0]
                distances = result.get("distances", [[0] * len(ids)])[0]
                for idx, doc_id in enumerate(ids):
                    try:
                        doc_pos = next(i for i, d in enumerate(documents) if d.metadata.get("file_id") == doc_id)
                        chroma_scores[doc_pos] = 1 - distances[idx]
                    except StopIteration:
                        continue
        except Exception:
            pass

    combined_scores = (
        0.34 * bm25_scores
        + 0.33 * cosine_sim_scores
        + 0.33 * chroma_scores
    )

    unique_top_document_indices = list(set(combined_scores.argsort()[::-1]))[:n_results]
    return [documents[i] for i in unique_top_document_indices]
