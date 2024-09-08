import os
import faiss
import numpy as np
from coderag.config import EMBEDDING_DIM, FAISS_INDEX_FILE, WATCHED_DIR

index = faiss.IndexFlatL2(EMBEDDING_DIM)
metadata = []

def clear_index():
    """Delete the FAISS index and metadata files if they exist, and reinitialize the index."""
    global index, metadata
    
    # Delete the FAISS index file
    if os.path.exists(FAISS_INDEX_FILE):
        os.remove(FAISS_INDEX_FILE)
        print(f"Deleted FAISS index file: {FAISS_INDEX_FILE}")

    # Delete the metadata file
    metadata_file = "metadata.npy"
    if os.path.exists(metadata_file):
        os.remove(metadata_file)
        print(f"Deleted metadata file: {metadata_file}")

    # Reinitialize the FAISS index and metadata
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    metadata = []
    print("FAISS index and metadata cleared and reinitialized.")

def add_to_index(embeddings, full_content, filename, filepath):
    global index, metadata

    if embeddings.shape[1] != index.d:
        raise ValueError(f"Embedding dimension {embeddings.shape[1]} does not match FAISS index dimension {index.d}")

    # Convert absolute filepath to relative path
    relative_filepath = os.path.relpath(filepath, WATCHED_DIR)

    index.add(embeddings)
    metadata.append({
        "content": full_content,
        "filename": filename,
        "filepath": relative_filepath  # Store relative filepath
    })

def save_index():
    faiss.write_index(index, FAISS_INDEX_FILE)
    with open("metadata.npy", "wb") as f:
        np.save(f, metadata)

def load_index():
    global index, metadata
    index = faiss.read_index(FAISS_INDEX_FILE)
    with open("metadata.npy", "rb") as f:
        metadata = np.load(f, allow_pickle=True).tolist()
    return index

def get_metadata():
    return metadata

def retrieve_vectors(n=5):
    n = min(n, index.ntotal)
    vectors = np.zeros((n, EMBEDDING_DIM), dtype=np.float32)
    for i in range(n):
        vectors[i] = index.reconstruct(i)
    return vectors

def inspect_metadata(n=5):
    metadata = get_metadata()
    print(f"Inspecting the first {n} metadata entries:")
    for i, data in enumerate(metadata[:n]):
        print(f"Entry {i}:")
        print(f"Filename: {data['filename']}")
        print(f"Filepath: {data['filepath']}")
        print(f"Content: {data['content'][:100]}...")  # Show the first 100 characters
        print()
