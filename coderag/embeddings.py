from openai import OpenAI
import numpy as np
from coderag.config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_embeddings(text):
    """Generate embeddings using the updated OpenAI API."""
    try:
        response = client.embeddings.create(
            model=OPENAI_EMBEDDING_MODEL,
            input=[text]  # Input should be a list of strings
        )
        # Extract the embedding from the response
        embeddings = response.data[0].embedding
        return np.array(embeddings).astype('float32').reshape(1, -1)
    except Exception as e:
        print(f"Error generating embeddings with OpenAI: {e}")
        return None