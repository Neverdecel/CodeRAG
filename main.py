import os
import logging
import atexit
import warnings
from coderag.index import clear_index, add_to_index, save_index
from coderag.embeddings import generate_embeddings
from coderag.config import WATCHED_DIR
from coderag.monitor import start_monitoring, should_ignore_path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Suppress transformers warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

def full_reindex():
    """Perform a full reindex of the entire codebase."""
    logging.info("Starting full reindexing of the codebase...")
    files_processed = 0
    for root, _, files in os.walk(WATCHED_DIR):
        if should_ignore_path(root):  # Check if the directory should be ignored
            logging.info(f"Ignoring directory: {root}")
            continue

        for file in files:
            filepath = os.path.join(root, file)
            if should_ignore_path(filepath):  # Check if the file should be ignored
                logging.info(f"Ignoring file: {filepath}")
                continue

            if file.endswith(".py"):
                logging.info(f"Processing file: {filepath}")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        full_content = f.read()

                    embeddings = generate_embeddings(full_content)  # Generate embeddings
                    if embeddings is not None:
                        add_to_index(embeddings, full_content, file, filepath)
                    else:
                        logging.warning(f"Failed to generate embeddings for {filepath}")
                    files_processed += 1
                except Exception as e:
                    logging.error(f"Error processing file {filepath}: {e}")

    save_index()
    logging.info(f"Full reindexing completed. {files_processed} files processed.")

def main():
    # Completely clear the FAISS index and metadata
    clear_index()

    # Perform a full reindex of the codebase
    full_reindex()

    # Start monitoring the directory for changes
    start_monitoring()

if __name__ == "__main__":
    main()