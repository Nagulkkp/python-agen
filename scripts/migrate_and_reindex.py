"""
scripts/migrate_and_reindex.py
==============================
One-click data migration utility that:
1. Re-chunks all clinical SOPs & module knowledge docs via MarkdownStructureSplitter.
2. Performs clean rebuild of ChromaDB collection 'himes_clinical_knowledge'.
3. Syncs and updates Valkey metadata schema with RAG routing section tags.
"""

import sys
import os
from pathlib import Path

# Ensure UTF-8 stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from config.settings import settings
from chunking.structure_splitter import MarkdownStructureSplitter
from vectorstore.chroma_manager import chroma_manager
from retrieval.hybrid_search import hybrid_search_engine
from valkey_himes_manager import valkey_manager

def run_migration():
    print("=" * 70)
    print("🚀 HIMES HYBRID RAG DATA MIGRATION & RE-INDEXING UTILITY")
    print("=" * 70)

    splitter = MarkdownStructureSplitter(
        target_words=settings.CHUNK_SIZE,
        overlap_words=settings.CHUNK_OVERLAP
    )

    # 1. Clean Rebuild of ChromaDB
    print("\n1. Rebuilding ChromaDB Collection...")
    chroma_manager.rebuild_collection()
    print(f"   Collection '{settings.COLLECTION_NAME}' re-created at {settings.CHROMA_PERSIST_DIR}.")

    # 2. Parse & Chunk Clinical SOPs
    all_chunks = []
    sop_dir = settings.CLINICAL_KNOWLEDGE_DIR
    md_files = list(sop_dir.glob("*.md")) if sop_dir.exists() else []

    print(f"\n2. Processing {len(md_files)} Clinical SOP files...")
    for md_path in md_files:
        try:
            with open(md_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            file_chunks = splitter.split_document(content, default_title=md_path.stem)
            all_chunks.extend(file_chunks)
            print(f"   • {md_path.name}: {len(file_chunks)} structured chunks.")
        except Exception as e:
            print(f"   ❌ Error reading {md_path.name}: {e}")

    # 3. Process All Modules Complete Knowledge (if present)
    modules_doc = settings.BASE_DIR / "all_modules_complete_knowledge.md"
    if modules_doc.exists():
        print(f"\n3. Processing Architectural Knowledge ({modules_doc.name})...")
        try:
            with open(modules_doc, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            mod_chunks = splitter.split_document(content, default_title="HIMES Module Architecture")
            all_chunks.extend(mod_chunks)
            print(f"   • Extracted {len(mod_chunks)} chunks from module architecture.")
        except Exception as e:
            print(f"   ❌ Error reading {modules_doc.name}: {e}")

    # 4. Upsert into ChromaDB
    print(f"\n4. Upserting {len(all_chunks)} total chunks into ChromaDB...")
    upserted_count = chroma_manager.upsert_chunks(all_chunks)
    print(f"   ✅ Successfully indexed {upserted_count} chunks with HNSW vector embeddings.")

    # 5. Build In-Memory BM25 Index
    print("\n5. Initializing BM25 Index over fresh corpus...")
    hybrid_search_engine.build_bm25_index_from_store()
    print(f"   ✅ BM25 Index compiled over {hybrid_search_engine.bm25_index.doc_count} documents.")

    # 6. Valkey Schema Synchronization & Metadata Enrichment
    print("\n6. Synchronizing Valkey Schema with RAG Section Tags...")
    screen_mappings = {
        "viewglobaloppharmacy": {"rag_tag": "Pharmacy & Antibiotic Stewardship", "module": "pharmacy"},
        "pricelistmanagement": {"rag_tag": "Billing & Tariff Masters", "module": "billing"},
        "viewlaboratoryworklist": {"rag_tag": "LIS Analytical Testing & Panic SOP", "module": "lis"},
        "viewpatientregistration": {"rag_tag": "Patient Registration & Triage", "module": "registration"}
    }
    
    valkey_updated = 0
    for screen_route, meta in screen_mappings.items():
        v_key = f"himes:screen:{screen_route}"
        existing = valkey_manager._get(v_key) or {}
        existing.update(meta)
        valkey_manager._set(v_key, existing, ttl=86400 * 7)
        valkey_updated += 1

    print(f"   ✅ Valkey updated: {valkey_updated} screens enriched with RAG knowledge section tags.")
    print("\n" + "=" * 70)
    print("✨ HYBRID RAG RE-INDEXING & MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_migration()
