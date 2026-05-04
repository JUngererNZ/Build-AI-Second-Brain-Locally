import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
INBOX = "./inbox"
VAULT = "./vault"

class LibrarianHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            print(f"📁 New knowledge detected: {filename}")
            
            # 1. Processing Logic (e.g., convert PDF to text or clean markdown)
            # For now, we simply move it to the Vault
            dest_path = os.path.join(VAULT, filename)
            shutil.move(event.src_path, dest_path)
            
            # 2. Trigger Indexing (You would call your Vector DB function here)
            print(f"✅ {filename} moved to Vault and ready for indexing.")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(LibrarianHandler(), INBOX, recursive=False)
    observer.start()
    print("🧠 Second Brain Librarian is watching the inbox...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()