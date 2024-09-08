import os
import subprocess
import atexit
import warnings
from coderag.index import clear_index, add_to_index, save_index
from coderag.embeddings import generate_embeddings  # Ensure this is imported
from coderag.config import WATCHED_DIR
from coderag.monitor import start_monitoring, should_ignore_path

# Suppress transformers warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

def full_reindex():
    """Perform a full reindex of the entire codebase."""
    print("Starting full reindexing of the codebase...")
    files_processed = 0
    for root, _, files in os.walk(WATCHED_DIR):
        if should_ignore_path(root):  # Check if the directory should be ignored
            print(f"Ignoring directory: {root}")
            continue
        
        for file in files:
            filepath = os.path.join(root, file)
            if should_ignore_path(filepath):  # Check if the file should be ignored
                print(f"Ignoring file: {filepath}")
                continue

            if file.endswith(".py"):
                print(f"Processing file: {filepath}")
                with open(filepath, 'r', encoding='utf-8') as f:
                    full_content = f.read()

                embeddings = generate_embeddings(full_content)  # Generate embeddings
                if embeddings is not None:
                    add_to_index(embeddings, full_content, file, filepath)
                else:
                    print(f"Failed to generate embeddings for {filepath}")
                files_processed += 1

    save_index()
    print(f"Full reindexing completed. {files_processed} files processed.")

def start_streamlit():
    """Start the Streamlit app in a separate thread."""
    print("Starting the Streamlit app...")
    subprocess.run(["streamlit", "run", "app.py"])

def main():
    # Completely clear the FAISS index and metadata
    clear_index()

    # Perform a full reindex of the codebase
    full_reindex()

    # Start the Streamlit app
    start_streamlit()

    # Start monitoring the directory for changes
    start_monitoring()

if __name__ == "__main__":
    main()
