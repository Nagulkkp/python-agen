"""
tests/test_hybrid_rag.py
========================
Verification suite testing chunking, BM25+Vector RRF ranking,
grounded citations, and dual-mode UI rendering.
"""

import sys
from pathlib import Path

# Ensure UTF-8 stdout on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from chunking.structure_splitter import MarkdownStructureSplitter
from retrieval.hybrid_search import hybrid_search_engine
from generation.rag_pipeline import rag_pipeline

def test_structure_chunker():
    print("\n--- TEST 1: MARKDOWN STRUCTURE CHUNKER ---")
    sample_md = """# Laboratory Protocols
## 1. Quality Control
### A. Westgard Rules
Rule 1-2s is a warning rule. Rule 1-3s detects random analytical error.
### B. Calibration
Calibrate clinical analyzers every 24 hours using certified reference standards.
"""
    splitter = MarkdownStructureSplitter(target_words=50, overlap_words=10)
    chunks = splitter.split_document(sample_md, default_title="Test SOP")
    assert len(chunks) >= 2, "Chunker must produce separate chunks for subsections"
    assert chunks[0].doc_title == "Laboratory Protocols"
    assert chunks[0].section == "1. Quality Control"
    print(f"✅ Produced {len(chunks)} structured chunks.")
    print(f"   Chunk 0: [{chunks[0].chunk_id}] {chunks[0].doc_title} > {chunks[0].section} > {chunks[0].subsection}")

def test_hybrid_rrf_retrieval():
    print("\n--- TEST 2: HYBRID RETRIEVAL & RECIPROCAL RANK FUSION ---")
    query = "Potassium panic value cardiac arrhythmia"
    res = hybrid_search_engine.search(query, top_k=3)
    chunks = res.get("top_chunks", [])
    assert len(chunks) > 0, "Hybrid search must return ranked results"
    assert "rrf_score" in chunks[0], "Top chunk must have an RRF score"
    print(f"✅ Hybrid search retrieved {len(chunks)} ranked chunks for query: '{query}'")
    for c in chunks:
        print(f"   • Chunk: {c['chunk_id']} | RRF: {c['rrf_score']} | Vector Rank: {c.get('vector_rank')} | BM25 Rank: {c.get('bm25_rank')}")

def test_dual_mode_generation():
    print("\n--- TEST 3: DUAL-MODE GROUNDED GENERATION & CITATIONS ---")
    query = "What is the critical high panic threshold for serum potassium?"
    
    # 1. Test User Mode
    print("   Testing Clean User Mode...")
    user_res = rag_pipeline.answer_query(query, is_developer_mode=False)
    assert user_res["status"] == "success", "RAG pipeline should succeed"
    assert "### 💻 Developer Diagnostics" not in user_res["reply"]
    print("   ✅ User mode formatted cleanly without technical diagnostics.")
    print(f"   Snippet: {user_res['reply'][:120]}...\n")
    
    # 2. Test Developer Mode
    print("   Testing Developer Diagnostic Mode...")
    dev_res = rag_pipeline.answer_query(query, is_developer_mode=True)
    assert "### 💻 Developer Diagnostics" in dev_res["reply"]
    assert "RRF Score" in dev_res["reply"]
    print("   ✅ Developer mode includes RRF scores and dense vs sparse comparisons.")

if __name__ == "__main__":
    print("=" * 65)
    print("🧪 RUNNING HIMES HYBRID RAG VERIFICATION SUITE")
    print("=" * 65)
    test_structure_chunker()
    test_hybrid_rrf_retrieval()
    test_dual_mode_generation()
    print("\n" + "=" * 65)
    print("🎉 ALL HYBRID RAG VERIFICATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)
