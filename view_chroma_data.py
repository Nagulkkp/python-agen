import os
import sys
import chromadb
import sqlite3
import json

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CHROMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_data")
DB_FILE = os.path.join(CHROMA_DIR, "chroma.sqlite3")

def view_chromadb_details():
    print("=" * 65)
    print(" CHROMADB STORAGE & CACHE INSPECTOR")
    print("=" * 65)
    print(f"Database Directory: {CHROMA_DIR}")
    print(f"Database File:      {DB_FILE}")
    if not os.path.exists(DB_FILE):
        print("chroma.sqlite3 not found yet.")
        return

    # 1. Connect via ChromaDB High-Level Client
    print("\n--- 1. COLLECTIONS & STORED DOCUMENTS ---")
    try:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        collections = client.list_collections()
        if not collections:
            print("No collections created yet.")
        for col in collections:
            print(f"\n[Collection: {col.name}] (Total Items: {col.count()})")
            items = col.get()
            count = len(items.get("ids", []))
            if count == 0:
                print("   (Empty - no records yet)")
            else:
                for i in range(count):
                    doc_id = items["ids"][i]
                    doc_text = items["documents"][i] if items["documents"] else ""
                    metadata = items["metadatas"][i] if items["metadatas"] else {}
                    print(f"   * ID: {doc_id}")
                    print(f"     Text / Query: {doc_text}")
                    if metadata:
                        print(f"     Metadata: {json.dumps(metadata, indent=6)}")
    except Exception as e:
        print(f"Error accessing ChromaDB client: {e}")

    # 2. Inspect Underlying SQLite Database Tables
    print("\n--- 2. INTERNAL SQLITE DATABASE TABLES ---")
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Found {len(tables)} tables in chroma.sqlite3:")
        for t in tables:
            cursor.execute(f"SELECT COUNT(*) FROM [{t}];")
            row_count = cursor.fetchone()[0]
            print(f"   • {t.ljust(25)} : {row_count} rows")
        conn.close()
    except Exception as e:
        print(f"Error reading SQLite tables: {e}")

    print("\n" + "=" * 65)

if __name__ == "__main__":
    view_chromadb_details()
