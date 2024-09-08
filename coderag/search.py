import numpy as np
from coderag.index import load_index, get_metadata
from coderag.embeddings import generate_embeddings

def search_code(query, k=5):
    """Search the FAISS index using a text query."""
    index = load_index()  # Load the FAISS index
    query_embedding = generate_embeddings(query)  # Generate embedding for the query

    if query_embedding is None:
        print("Failed to generate query embedding.")
        return []

    # Perform the search in FAISS
    distances, indices = index.search(query_embedding, k)

    results = []
    for i, idx in enumerate(indices[0]):  # Iterate over the search results
        if idx < len(get_metadata()):  # Ensure the index is within bounds
            file_data = get_metadata()[idx]
            results.append({
                "filename": file_data["filename"],
                "filepath": file_data["filepath"],
                "content": file_data["content"],
                "distance": distances[0][i]  # Access distance using the correct index
            })
        else:
            print(f"Warning: Index {idx} is out of bounds for metadata with length {len(get_metadata())}")
    return results
