import hashlib
from src.archivagent.ingestion.parser import DBLPStreamParser
from src.archivagent.vector_db.client import VectorStore

class IngestionPipeline:
    def __init__(self):
        self.parser = DBLPStreamParser("data/raw/dblp.xml.gz", target_year=None, batch_size=100)
        self.db = VectorStore()

    def run_test_ingestion(self, max_batches: int = 100):
        print("Starting the ingestion pipeline...")
        
        for batch_idx, batch in enumerate(self.parser.parse_stream()):
            if batch_idx >= max_batches:
                break
                
            print(f"\nProcessing Batch {batch_idx + 1} ({len(batch)} records)...")
            
            documents = []
            metadatas = []
            ids = []
            
            # 1. Track IDs to prevent duplicate insertion within the same batch
            seen_batch_ids = set()
            
            for record in batch:
                unique_hash = hashlib.md5(f"{record.title}{record.year}".encode()).hexdigest()
                doc_id = f"doc_{unique_hash}"
                
                # If we already generated this ID in this batch, skip the duplicate
                if doc_id in seen_batch_ids:
                    continue
                    
                seen_batch_ids.add(doc_id)
                
                authors_str = ", ".join([author.name for author in record.authors])
                doc_text = (
                    f"Title: {record.title}\n"
                    f"Authors: {authors_str}\n"
                    f"Venue: {record.venue}\n"
                    f"Category: {record.category}\n"
                )
                documents.append(doc_text)
                
                metadatas.append({
                    "title": record.title,
                    "venue": record.venue,
                    "year": record.year,
                    "category": record.category
                })
                
                ids.append(doc_id)
                
            print(f"Embedding and inserting batch into ChromaDB via Ollama...")
            
            # 2. Use 'upsert' instead of 'add' to safely bypass records we already ingested
            self.db.collection.upsert(documents=documents, metadatas=metadatas, ids=ids)
            
            print(f"Batch {batch_idx + 1} successfully embedded!")
            
        print("\nPipeline test complete.")
        print(f"Total embedded document count in database: {self.db.collection.count()}")

# --- Testing Block ---
if __name__ == "__main__":
    pipeline = IngestionPipeline()
    pipeline.run_test_ingestion(max_batches=100)
