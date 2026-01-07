import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_chunks(extracted_data, chunk_size=500, overlap=50):
    """Splits structured text into overlapping chunks with metadata."""
    chunks = []
    
    for item in extracted_data:
        text = item.get('text', '')
        page_num = item.get('page', 0)
        
        words = text.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk_text = " ".join(words[i:i + chunk_size])
            chunks.append({
                'text': chunk_text,
                'page': page_num
            })
            
    return chunks

def build_index(extracted_data):
    """Builds a FAISS index from structured extracted data."""
    chunks = create_chunks(extracted_data)
    if not chunks:
        return None, []
    
    # Extract just the text for embedding
    texts = [c['text'] for c in chunks]
    
    embeddings = model.encode(texts)
    dimension = embeddings.shape[1]
    
    faiss.normalize_L2(embeddings)
    
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    return index, chunks

def search_index(query, index, chunks, k=5):
    """Searches the index for the query."""
    if not index or not chunks:
        return []
    
    query_embedding = model.encode([query])
    faiss.normalize_L2(query_embedding)
    
    D, I = index.search(query_embedding, k)
    
    results = []
    for i, idx in enumerate(I[0]):
        if idx != -1 and idx < len(chunks):
            chunk = chunks[idx]
            results.append({
                'score': float(D[0][i]),
                'text': chunk['text'],
                'page': chunk['page']
            })
    return results

def save_precomputed(index, chunks, base_path):
    """Saves index and chunks to disk."""
    faiss.write_index(index, base_path + ".index")
    with open(base_path + ".chunks", "wb") as f:
        pickle.dump(chunks, f)

def load_precomputed(base_path):
    """Loads index and chunks from disk."""
    if not os.path.exists(base_path + ".index") or not os.path.exists(base_path + ".chunks"):
        return None, None
    
    index = faiss.read_index(base_path + ".index")
    with open(base_path + ".chunks", "rb") as f:
        chunks = pickle.load(f)
    return index, chunks
