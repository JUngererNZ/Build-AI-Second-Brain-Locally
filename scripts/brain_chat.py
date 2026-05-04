import ollama
import chromadb
import sys

# --- CONFIGURATION ---
DB_PATH = "./db"
COLLECTION_NAME = "second_brain"
EMBED_MODEL = "nomic-embed-text:latest"
CHAT_MODEL = "qwen2.5:7b" # Optimized for your current local model list

# Initialize ChromaDB
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(name=COLLECTION_NAME)

def query_brain(user_query):
    # 1. Generate embedding for the question
    print("🔍 Searching through your knowledge...")
    response = ollama.embeddings(model=EMBED_MODEL, prompt=user_query)
    query_embedding = response["embedding"]

    # 2. Retrieve the top 5 most relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    # 3. Consolidate retrieved text into a context block
    context = "\n\n---\n\n".join(results["documents"][0])
    sources = list(set([m["source"] for m in results["metadatas"][0]]))

    # 4. Construct the prompt for the LLM
    system_prompt = (
        "You are a private AI Second Brain. Use the provided context from the user's "
        "personal files to answer the question. If the answer is not in the context, "
        "say you don't know based on your current knowledge. Be concise."
    )
    
    full_prompt = f"CONTEXT:\n{context}\n\nQUESTION: {user_query}"

    # 5. Generate the answer using your local LLM
    print(f"🧠 {CHAT_MODEL} is thinking...")
    chat_response = ollama.chat(model=CHAT_MODEL, messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': full_prompt},
    ])

    # 6. Output the results
    print("\n" + "="*30)
    print("AI RESPONSE:")
    print(chat_response['message']['content'])
    print("="*30)
    print(f"SOURCES: {', '.join(sources)}")
    print("="*30 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run a single query from command line arguments
        query_brain(" ".join(sys.argv[1:]))
    else:
        # Start an interactive loop
        print("Welcome to your Local Second Brain. (Type 'exit' to quit)")
        while True:
            q = input("❓ Ask anything: ")
            if q.lower() in ['exit', 'quit']:
                break
            query_brain(q)