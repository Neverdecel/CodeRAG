import faiss
from coderag.index import load_index, retrieve_vectors, inspect_metadata, add_to_index, save_index, clear_index
from coderag.embeddings import generate_embeddings
import os

def test_faiss_index():
    # Clear the index before testing
    clear_index()

    # Example text to generate embeddings
    example_text = "This is a test document to be indexed."

    # Generate embeddings
    embeddings = generate_embeddings(example_text)
    if embeddings is None:
        print("Embedding generation failed.")
        return

    # Add to index
    add_to_index(embeddings, example_text, "test_file.py", "test_file.py")
    save_index()

    # Load the index
    index = load_index()

    # Check if index has vectors
    assert index.ntotal > 0, "FAISS index is empty. No vectors found!"
    print(f"FAISS index has {index.ntotal} vectors.")

    # Retrieve and inspect vectors
    vectors = retrieve_vectors(5)
    print(f"Retrieved {len(vectors)} vectors from the index.")
    
    # Inspect metadata
    inspect_metadata(5)

if __name__ == "__main__":
    test_faiss_index()
