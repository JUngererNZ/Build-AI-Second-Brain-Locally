import os
import shutil
import chromadb
import ollama
from pypdf import PdfReader

# --- Configuration ---
INBOX_PATH = "./inbox"
VAULT_PATH = "./vault"
DB_PATH = "./db"
COLLECTION_NAME = "second_brain"
EMBED_MODEL = "nomic-embed-text:latest"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# Initialize ChromaDB (Persistent)
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def move_from_inbox():
    """Moves all files from inbox/ to vault/ before indexing."""
    if not os.path.exists(INBOX_PATH):
        os.makedirs(INBOX_PATH)
        return

    entries = os.listdir(INBOX_PATH)
    if not entries:
        print("📥 Inbox is empty. Proceeding to vault check...")
        return

    print(f"🚚 Found {len(entries)} items in inbox. Moving files to vault...")
    for name in entries:
        source = os.path.join(INBOX_PATH, name)

        # Skip directories; only move plain files
        if os.path.isdir(source):
            print(f"📁 Skipping directory in inbox: {name}")
            continue

        destination = os.path.join(VAULT_PATH, name)

        # Handle potential filename collisions
        if os.path.exists(destination):
            print(f"⚠️ {name} already exists in vault. Skipping move.")
            continue

        try:
            shutil.move(source, destination)
            print(f"✅ Moved: {name}")
        except Exception as e:
            print(f"❌ Failed to move {name}: {e}")


def cleanup_inbox():
    """Final safety: remove any leftover files and empty folders in inbox/."""
    if not os.path.exists(INBOX_PATH):
        return

    # Delete remaining files
    for root, dirs, files in os.walk(INBOX_PATH, topdown=False):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                os.remove(fpath)
                print(f"🗑️ Deleted leftover file from inbox: {fpath}")
            except Exception as e:
                print(f"❌ Failed to delete {fpath}: {e}")

        # Remove empty directories
        for dname in dirs:
            dpath = os.path.join(root, dname)
            try:
                if not os.listdir(dpath):
                    os.rmdir(dpath)
                    print(f"🧹 Removed empty folder from inbox: {dpath}")
            except Exception as e:
                print(f"❌ Failed to remove folder {dpath}: {e}")


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
                text = page.extract_text()
                if text:
                    content += text + "\n"
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
    return content


def chunk_text(text):
    """Splits text into smaller pieces for better retrieval."""
    chunks = []
    for i in range(0, len(text), CHUNK_SIZE - CHUNK_OVERLAP):
        chunks.append(text[i: i + CHUNK_SIZE])
    return chunks


def index_vault():
    """Main loop to move from inbox and then process files in the vault."""
    # Step 1: Sweep the inbox (this should leave inbox/ with only odd leftovers)
    move_from_inbox()

    print("🚀 Starting indexing process...")

    # Refresh file list after move
    vault_files = os.listdir(VAULT_PATH)

    for filename in vault_files:
        file_path = os.path.join(VAULT_PATH, filename)

        if os.path.isdir(file_path):
            continue

        print(f"📖 Processing: {filename}")
        raw_text = extract_text(file_path)

        if not raw_text.strip():
            print(f"⚠️ Skipping empty or unreadable file: {filename}")
            continue

        chunks = chunk_text(raw_text)

        for i, chunk in enumerate(chunks):
            # Generate the embedding via Ollama
            response = ollama.embeddings(model=EMBED_MODEL, prompt=chunk)
            embedding = response["embedding"]

            # Upsert ensures we don't get 'ID already exists' errors
            collection.upsert(
                ids=[f"{filename}_{i}"],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": filename, "chunk_index": i}],
            )

    # Step 3: final clean-up so inbox/ is guaranteed empty
    cleanup_inbox()
    print("✨ Indexing complete. Inbox is clean and knowledge is searchable!")


if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs(INBOX_PATH, exist_ok=True)
    os.makedirs(VAULT_PATH, exist_ok=True)
    index_vault()