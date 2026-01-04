"""
Cache Manager Module
Handles repository caching operations for faster repeated access.
"""

import os
import hashlib
import pickle
import time
import shutil


def get_repo_hash(repo_url):
    """Generate a hash for the repository URL"""
    return hashlib.md5(repo_url.encode()).hexdigest()


def get_cache_path(repo_url, cache_dir):
    """Get the cache directory path for a repository"""
    repo_hash = get_repo_hash(repo_url)
    return os.path.join(cache_dir, repo_hash)


def is_repo_cached(repo_url, cache_dir):
    """Check if repository is already cached"""
    cache_path = get_cache_path(repo_url, cache_dir)
    return os.path.exists(cache_path) and os.path.exists(os.path.join(cache_path, "cache_data.pkl"))


def save_repo_cache(repo_url, cache_dir, index, document, file_type_count, file_names):
    """Save repository processing results to cache"""
    cache_path = get_cache_path(repo_url, cache_dir)
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    
    # Drop non-serializable Chroma objects; keep collection name for reload
    if isinstance(index, dict) and index.get("chroma_collection") is not None:
        index = {k: v for k, v in index.items() if k != "chroma_collection"}

    cache_data = {
        'index': index,
        'document': document,
        'file_type_count': file_type_count,
        'file_names': file_names,
        'timestamp': time.time()
    }
    
    with open(os.path.join(cache_path, "cache_data.pkl"), 'wb') as f:
        pickle.dump(cache_data, f)


def load_repo_cache(repo_url, cache_dir):
    """Load repository processing results from cache"""
    cache_path = get_cache_path(repo_url, cache_dir)
    cache_file = os.path.join(cache_path, "cache_data.pkl")
    
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            cache_data = pickle.load(f)
        index = cache_data['index']
        return index, cache_data['document'], cache_data['file_type_count'], cache_data['file_names']
    return None, None, None, None


def clear_old_cache(cache_dir, max_age_hours=24):
    """Clear cache files older than specified hours"""
    if not os.path.exists(cache_dir):
        return
    
    current_time = time.time()
    for cache_folder in os.listdir(cache_dir):
        cache_path = os.path.join(cache_dir, cache_folder)
        cache_file = os.path.join(cache_path, "cache_data.pkl")
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                
                if current_time - cache_data['timestamp'] > max_age_hours * 3600:
                    shutil.rmtree(cache_path)
                    print(f"Cleared old cache for {cache_folder}")
            except:
                # If we can't read the cache file, remove it
                shutil.rmtree(cache_path)
