from coderag.index import save_index

def initialize_index():
    save_index()
    print("FAISS index initialized and saved.")

if __name__ == "__main__":
    initialize_index()
