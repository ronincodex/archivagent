import chromadb
from chromadb.utils import embedding_functions

class VectorStore:
    def __init__(self, persist_directory: str = "vector_db"):
        """Initializes the persistent local Chroma database."""
        # This securely stores the vector data on your local drive
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Configure the native Ollama integration directed at your CPU server
        self.embedding_fn = embedding_functions.OllamaEmbeddingFunction(
            url="http://127.0.0.1:11434/api/embeddings",
            model_name="nomic-embed-text"
        )
        
        # Create or load the deterministic storage collection
        self.collection = self.client.get_or_create_collection(
            name="literature_archive",
            embedding_function=self.embedding_fn
        )

    def add_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        """Batches and inserts vectorized documents into the collection."""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

# --- Testing Block ---
if __name__ == "__main__":
    print("Initializing persistent Vector Store...")
    db = VectorStore()
    
    print(f"Success! Collection '{db.collection.name}' is active.")
    print(f"Current embedded document count: {db.collection.count()}")
