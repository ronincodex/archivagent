import sys
import ollama
from src.archivagent.vector_db.client import VectorStore

class ArchivAgent:
    def __init__(self):
        self.db = VectorStore()
        self.generation_model = "qwen2.5:1.5b"
        # Initialize an empty list to store chat history
        self.conversation_history = []

    def query(self, user_question: str) -> str:
        # 1. Retrieve the most relevant documents
        results = self.db.collection.query(query_texts=[user_question], n_results=3)
        retrieved_docs = results['documents'][0]

        if not retrieved_docs:
            context = "No relevant documents found in the archive."
        else:
            context = "\n---\n".join(retrieved_docs)

        # 2. Construct the strict RAG system prompt
        system_prompt = (
            "You are a highly precise archiving assistant operating within a CLI environment. "
            "You must answer the user's question based strictly on the provided CONTEXT below. "
            "Do not hallucinate external information. If the answer is not in the context, say so clearly.\n\n"
            "CONTEXT:\n"
            f"{context}"
        )

        # 3. Build the payload with the system prompt, previous memory, and the new question
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.conversation_history)
        messages.append({"role": "user", "content": user_question})

        # 4. Generate the response
        response = ollama.chat(model=self.generation_model, messages=messages)
        ai_reply = response['message']['content']

        # 5. Save the interaction to memory for follow-up questions
        self.conversation_history.append({"role": "user", "content": user_question})
        self.conversation_history.append({"role": "assistant", "content": ai_reply})

        return ai_reply

# --- Product Interface (REPL Loop) ---
if __name__ == "__main__":
    agent = ArchivAgent()
    
    print("=" * 60)
    print(" 📚 ArchivAgent Terminal Interface Online")
    print(" Type your query to search the literature archive.")
    print(" Commands: 'clear' to wipe memory | 'exit' to close")
    print("=" * 60)

    # The continuous chat loop
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            # Ignore empty enter presses
            if not user_input:
                continue
                
            # Handle exit commands
            if user_input.lower() in ["exit", "quit", "q"]:
                print("\nShutting down ArchivAgent. Goodbye!")
                sys.exit(0)
                
            # Handle memory management
            if user_input.lower() == "clear":
                agent.conversation_history = []
                print("\n[*] Conversation memory wiped. Starting fresh.")
                continue

            # Process the query
            print("\n[*] ArchivAgent is searching and generating...")
            answer = agent.query(user_input)
            
            print(f"\nArchivAgent:\n{answer}")

        # Gracefully handle Ctrl+C or Ctrl+D exits
        except (KeyboardInterrupt, EOFError):
            print("\n\nShutting down ArchivAgent. Goodbye!")
            sys.exit(0)
