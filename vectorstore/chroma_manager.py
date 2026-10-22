"""
vectorstore/chroma_manager.py
=============================
Encapsulates ChromaDB persistent client initialization, HNSW index 
configuration, full collection rebuilding, and atomic upsert operations.
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.utils import embedding_functions

from config.settings import settings
from chunking.structure_splitter import DocumentChunk

class ChromaManager:
    _instance: Optional["ChromaManager"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.persist_dir = str(settings.CHROMA_PERSIST_DIR)
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        
        # Fast, deterministic local ONNX MiniLM embedding function (zero API latency)
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": settings.HNSW_SPACE}
        )

    def rebuild_collection(self) -> None:
        """Wipes and re-creates the collection for clean re-indexing."""
        try:
            self.client.delete_collection(name=settings.COLLECTION_NAME)
        except Exception:
            pass
        self.collection = self.client.create_collection(
            name=settings.COLLECTION_NAME,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": settings.HNSW_SPACE}
        )

    def upsert_chunks(self, chunks: List[DocumentChunk], batch_size: int = 64) -> int:
        """
        Batch upserts DocumentChunk instances into ChromaDB.
        Avoids payload limits with chunked batch iterations.
        """
        if not chunks:
            return 0

        total_upserted = 0
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            ids = [c.chunk_id for c in batch]
            documents = [c.text for c in batch]
            metadatas = [c.to_metadata() for c in batch]

            self.collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            total_upserted += len(batch)

        return total_upserted

    def vector_search(self, query: str, limit: int = 15) -> List[Dict[str, Any]]:
        """
        Performs dense semantic vector similarity search.
        Returns normalized similarity records.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=limit
        )

        formatted: List[Dict[str, Any]] = []
        if not results or not results["ids"] or not results["ids"][0]:
            return formatted

        ids = results["ids"][0]
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        dists = results["distances"][0]

        for rank, (chunk_id, doc, meta, dist) in enumerate(zip(ids, docs, metas, dists), start=1):
            formatted.append({
                "chunk_id": chunk_id,
                "text": doc,
                "metadata": meta,
                "vector_distance": dist,
                "vector_rank": rank
            })

        return formatted

    def get_all_documents(self) -> Dict[str, Any]:
        """Fetches all documents and IDs for building sparse index."""
        return self.collection.get(include=["documents", "metadatas"])

chroma_manager = ChromaManager()
