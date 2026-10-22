"""
retrieval/hybrid_search.py
==========================
High-performance Hybrid Search Engine combining:
1. BM25 Lexical Keyword Search (exact medical terminology, tube names, thresholds).
2. ChromaDB Dense Semantic Search (conceptual clinical relationships).
3. Reciprocal Rank Fusion (RRF) for principled score unification.
"""

import math
import re
from typing import List, Dict, Any
from collections import Counter

from config.settings import settings
from vectorstore.chroma_manager import chroma_manager

class LocalBM25Index:
    """
    Self-contained, zero-dependency BM25 Okapi implementation 
    optimized for fast in-memory execution over clinical documents.
    """
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_ids: List[str] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_count: int = 0
        self.doc_freqs: Dict[str, int] = Counter()
        self.inverted_index: List[Counter] = []

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\b[a-zA-Z0-9_\-+#.]+\b", text.lower())

    def fit(self, doc_ids: List[str], documents: List[str]):
        self.corpus_ids = doc_ids
        self.doc_count = len(documents)
        self.doc_lengths = []
        self.doc_freqs = Counter()
        self.inverted_index = []

        total_words = 0
        for doc in documents:
            tokens = self._tokenize(doc)
            t_len = len(tokens)
            self.doc_lengths.append(t_len)
            total_words += t_len
            
            tf = Counter(tokens)
            self.inverted_index.append(tf)
            for token in tf.keys():
                self.doc_freqs[token] += 1

        self.avg_doc_len = total_words / self.doc_count if self.doc_count > 0 else 1.0

    def search(self, query: str, limit: int = 15) -> List[Dict[str, Any]]:
        if self.doc_count == 0:
            return []

        tokens = self._tokenize(query)
        scores: List[float] = [0.0] * self.doc_count

        for token in tokens:
            df = self.doc_freqs.get(token, 0)
            if df == 0:
                continue
            # Standard Lucene/BM25 IDF formula
            idf = math.log(1.0 + (self.doc_count - df + 0.5) / (df + 0.5))

            for idx in range(self.doc_count):
                tf = self.inverted_index[idx].get(token, 0)
                if tf == 0:
                    continue
                num = tf * (self.k1 + 1.0)
                denom = tf + self.k1 * (1.0 - self.b + self.b * (self.doc_lengths[idx] / self.avg_doc_len))
                scores[idx] += idf * (num / denom)

        ranked_indices = sorted(
            [i for i in range(self.doc_count) if scores[i] > 0.0],
            key=lambda x: scores[x],
            reverse=True
        )[:limit]

        results = []
        for rank, idx in enumerate(ranked_indices, start=1):
            results.append({
                "chunk_id": self.corpus_ids[idx],
                "bm25_score": round(scores[idx], 4),
                "bm25_rank": rank
            })
        return results

class HybridSearchEngine:
    def __init__(self):
        self.bm25_index = LocalBM25Index()
        self._index_built = False

    def build_bm25_index_from_store(self):
        """Pulls all indexed documents from ChromaDB and builds the sparse BM25 index."""
        raw = chroma_manager.get_all_documents()
        ids = raw.get("ids", [])
        documents = raw.get("documents", [])
        if ids and documents:
            self.bm25_index.fit(ids, documents)
            self._index_built = True

    def search(self, query: str, top_k: int = settings.TOP_K) -> Dict[str, Any]:
        """
        Executes Dense + Sparse searches in parallel and fuses with RRF:
        RRF_Score(doc) = Sum( 1.0 / (RRF_K + rank) )
        """
        if not self._index_built:
            self.build_bm25_index_from_store()

        # 1. Fetch Candidates from Dense Vector & Sparse BM25
        dense_candidates = chroma_manager.vector_search(query, limit=settings.CANDIDATE_POOL_SIZE)
        sparse_candidates = self.bm25_index.search(query, limit=settings.CANDIDATE_POOL_SIZE)

        # 2. Reciprocal Rank Fusion
        fused_scores: Dict[str, float] = {}
        candidate_map: Dict[str, Dict[str, Any]] = {}

        # Merge Dense candidates
        for item in dense_candidates:
            c_id = item["chunk_id"]
            rrf_contrib = 1.0 / (settings.RRF_K + item["vector_rank"])
            fused_scores[c_id] = fused_scores.get(c_id, 0.0) + rrf_contrib
            candidate_map[c_id] = {
                "chunk_id": c_id,
                "text": item["text"],
                "metadata": item["metadata"],
                "vector_rank": item["vector_rank"],
                "vector_distance": item["vector_distance"],
                "bm25_rank": None,
                "bm25_score": 0.0
            }

        # Merge Sparse candidates
        for item in sparse_candidates:
            c_id = item["chunk_id"]
            rrf_contrib = 1.0 / (settings.RRF_K + item["bm25_rank"])
            fused_scores[c_id] = fused_scores.get(c_id, 0.0) + rrf_contrib
            
            if c_id in candidate_map:
                candidate_map[c_id]["bm25_rank"] = item["bm25_rank"]
                candidate_map[c_id]["bm25_score"] = item["bm25_score"]
            else:
                try:
                    c_data = chroma_manager.collection.get(ids=[c_id], include=["documents", "metadatas"])
                    text = c_data["documents"][0] if c_data.get("documents") else ""
                    meta = c_data["metadatas"][0] if c_data.get("metadatas") else {}
                except Exception:
                    text = ""
                    meta = {}
                candidate_map[c_id] = {
                    "chunk_id": c_id,
                    "text": text,
                    "metadata": meta,
                    "vector_rank": None,
                    "vector_distance": None,
                    "bm25_rank": item["bm25_rank"],
                    "bm25_score": item["bm25_score"]
                }

        # 3. Sort by aggregated RRF score
        sorted_ids = sorted(fused_scores.keys(), key=lambda x: fused_scores[x], reverse=True)[:top_k]

        final_ranked_chunks: List[Dict[str, Any]] = []
        for rank, c_id in enumerate(sorted_ids, start=1):
            entry = candidate_map[c_id]
            entry["rrf_score"] = round(fused_scores[c_id], 6)
            entry["final_rank"] = rank
            final_ranked_chunks.append(entry)

        return {
            "query": query,
            "top_chunks": final_ranked_chunks,
            "dense_count": len(dense_candidates),
            "sparse_count": len(sparse_candidates)
        }

hybrid_search_engine = HybridSearchEngine()
