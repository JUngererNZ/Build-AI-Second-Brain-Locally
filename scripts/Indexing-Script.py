# --- 1st try at creating such ---
import os
import chromadb
import ollama
from pypdf import PdfReader

# --- Configuration ---
VAULT_PATH = "./vault"
DB_PATH = "./db"
COLLECTION_NAME = "second_brain"
EMBED_MODEL = "nomic-embed-text"
CHUNK_SIZE = 1000  # Characters per chunk
CHUNK_OVERLAP = 100 # Overlap to keep context between chunks

# Initialize ChromaDB (Persistent)
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def extract_text(file_path):
    """Extracts text from Markdown, Text, and PDF files."""
    ext = os.path.splitext(file_path)[1].lower()
    content = ""
    try:
        if ext in [".md", ".txt"]:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        elif ext == ".pdf":
            reader = PdfReader(file_path)
            for page in reader.pages:
                content += page.extract_text() + "\n"
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
    return content

def chunk_text(text):
    """Splits text into smaller pieces for better retrieval."""
    chunks = []
    for i in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP):
        chunks.append(text[i : i + CHUNK_SIZE])
    return chunks

def index_vault():
    """Main loop to process files in the vault."""
    print("🚀 Starting indexing process...")
    
    for filename in os.listdir(VAULT_PATH):
        file_path = os.path.join(VAULT_PATH, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
            
        print(f"📖 Processing: {filename}")
        raw_text = extract_text(file_path)
        
        if not raw_text.strip():
            continue

        chunks = chunk_text(raw_text)
        
        for i, chunk in enumerate(chunks):
            # Generate the embedding (vector) via Ollama
            response = ollama.embeddings(model=EMBED_MODEL, prompt=chunk)
            embedding = response["embedding"]
            
            # Add to ChromaDB
            collection.add(
                ids=[f"{filename}_{i}"],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": filename, "chunk_index": i}]
            )

    print(f"✅ Indexing complete. Knowledge is now searchable!")

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs(VAULT_PATH, exist_ok=True)
    index_vault()