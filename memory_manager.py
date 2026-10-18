import os
import sys
import uuid
from typing import List, Dict, Any, Union, Optional
from dotenv import load_dotenv
import chromadb
from langchain_openai import OpenAIEmbeddings

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Load environment variables
load_dotenv(override=True)

# Define persistent storage directory for ChromaDB
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DATA_DIR = os.path.join(BASE_DIR, "chroma_data")
os.makedirs(CHROMA_DATA_DIR, exist_ok=True)

# Initialize local persistent ChromaDB client
chroma_client = chromadb.PersistentClient(path=CHROMA_DATA_DIR)
COLLECTION_NAME = "agent_knowledge_base"
collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine", "description": "Persistent memory and knowledge base for AI Agent"}
)

class UniversalEmbeddingWrapper:
    """
    Supports OpenAI text-embedding-3-small when OPENAI_API_KEY is available in .env,
    and seamlessly falls back to fast local ONNX embeddings (all-MiniLM-L6-v2) otherwise.
    """
    def __init__(self):
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and not openai_key.startswith("your_"):
            try:
                from langchain_openai import OpenAIEmbeddings
                self._model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=openai_key)
                self.mode = "OpenAI (text-embedding-3-small)"
                return
            except Exception:
                pass

        # Local ONNX fallback - works 100% offline without API keys
        from chromadb.utils import embedding_functions
        self._fn = embedding_functions.DefaultEmbeddingFunction()
        self.mode = "Local ONNX (all-MiniLM-L6-v2)"

    def embed_query(self, text: str) -> list:
        if hasattr(self, "_model"):
            return self._model.embed_query(text)
        return self._fn([text])[0]

    def embed_documents(self, texts: list) -> list:
        if hasattr(self, "_model"):
            return self._model.embed_documents(texts)
        return self._fn(texts)

_embeddings_instance: Optional[UniversalEmbeddingWrapper] = None

def get_embeddings_model() -> UniversalEmbeddingWrapper:
    """Lazily initializes and returns the embedding provider."""
    global _embeddings_instance
    if _embeddings_instance is None:
        _embeddings_instance = UniversalEmbeddingWrapper()
        print(f"ℹ️ ChromaDB Embedding Provider active: {_embeddings_instance.mode}")
    return _embeddings_instance


def add_to_knowledge_base(documents_list: List[Union[str, Dict[str, Any]]]) -> List[str]:
    """
    Takes text documents or logs, converts them into embeddings
    using OpenAI (text-embedding-3-small), and saves them in ChromaDB with unique IDs.

    Args:
        documents_list: A list of strings OR list of dicts with 'text' and optional 'metadata'.

    Returns:
        List of generated unique IDs for the saved documents.
    """
    if not documents_list:
        return []

    texts: List[str] = []
    metadatas: List[Dict[str, Any]] = []
    ids: List[str] = []

    for item in documents_list:
        doc_id = str(uuid.uuid4())
        ids.append(doc_id)

        if isinstance(item, dict):
            text_content = item.get("text") or item.get("content") or str(item)
            meta = item.get("metadata", {})
            if not isinstance(meta, dict):
                meta = {"raw_meta": str(meta)}
            texts.append(text_content)
            metadatas.append(meta)
        else:
            texts.append(str(item))
            metadatas.append({"source": "manual_entry"})

    # Convert documents into embeddings using OpenAI text-embedding-3-small
    embeddings = get_embeddings_model().embed_documents(texts)

    # Save documents, embeddings, and metadata into persistent ChromaDB
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f" Successfully added {len(ids)} document(s) to ChromaDB knowledge base.")
    return ids


def search_knowledge_base(user_query: str, limit: int = 3) -> List[Dict[str, Any]]:
    """
    Searches ChromaDB using semantic search and returns the most relevant documents.

    Args:
        user_query: The query text to search for semantically.
        limit: Maximum number of relevant documents to return (default: 3).

    Returns:
        A list of matching records, each containing 'id', 'document', 'metadata', and 'distance'.
    """
    if not user_query or not user_query.strip():
        return []

    total_docs = collection.count()
    if total_docs == 0:
        return []

    fetch_limit = min(limit, total_docs)

    # Convert the user query into an embedding using OpenAI text-embedding-3-small
    query_vector = get_embeddings_model().embed_query(user_query)

    # Perform semantic search on ChromaDB
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=fetch_limit,
        include=["documents", "metadatas", "distances"]
    )

    formatted_results = []
    if results and "documents" in results and results["documents"]:
        doc_list = results["documents"][0]
        id_list = results["ids"][0]
        meta_list = results.get("metadatas", [[]])[0] if results.get("metadatas") else [{}] * len(doc_list)
        dist_list = results.get("distances", [[]])[0] if results.get("distances") else [None] * len(doc_list)

        for doc_id, document, metadata, distance in zip(id_list, doc_list, meta_list, dist_list):
            formatted_results.append({
                "id": doc_id,
                "document": document,
                "metadata": metadata,
                "distance": distance
            })

    return formatted_results


if __name__ == "__main__":
    print("=" * 60)
    print("ChromaDB Memory Manager Test")
    print("=" * 60)
    print(f"Chroma Data Path: {CHROMA_DATA_DIR}")
    print(f"Current Docs in Knowledge Base: {collection.count()}")
