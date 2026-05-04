import ollama
import chromadb

# Initialize local Vector DB
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="second_brain")

def ask_brain(query):
    # 1. Generate embedding for the query
    query_emb = ollama.embeddings(model="nomic-embed-text", prompt=query)['embedding']
    
    # 2. Search for the top 3 relevant snippets in your vault
    results = collection.query(query_embeddings=[query_emb], n_results=3)
    context = "\n".join(results['documents'][0])
    
    # 3. Augment the prompt with your private data
    prompt = f"Using the following context from my notes, answer the question.\n\nContext: {context}\n\nQuestion: {query}"
    
    response = ollama.chat(model="llama4", messages=[
        {'role': 'system', 'content': 'You are a helpful AI Second Brain. Use the provided context to answer.'},
        {'role': 'user', 'content': prompt},
    ])
    
    return response['message']['content']

# Example usage
# print(ask_brain("What did I note down about the project deadline?"))