"""
config/settings.py
==================
Centralized configuration for the HIMES Hybrid RAG Engine.
Enforces Single Source of Truth; zero hardcoded magic numbers.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class RAGSettings(BaseSettings):
    # Base Directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    CLINICAL_KNOWLEDGE_DIR: Path = Path(__file__).resolve().parent.parent / "clinical_knowledge"
    CHROMA_PERSIST_DIR: Path = Path(__file__).resolve().parent.parent / "chroma_data"
    
    # ChromaDB Configuration
    COLLECTION_NAME: str = "himes_clinical_knowledge"
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    HNSW_SPACE: str = "cosine"
    
    # Structure Splitter Hyperparameters
    CHUNK_SIZE: int = 400            # Max word count target per chunk
    CHUNK_OVERLAP: int = 50          # Overlapping words between split chunks
    MIN_CHUNK_LENGTH: int = 20       # Discard chunks shorter than 20 characters
    
    # Hybrid Retrieval & RRF Hyperparameters
    TOP_K: int = 5                   # Final ranked documents passed to LLM
    CANDIDATE_POOL_SIZE: int = 15    # Intermediate candidate pool retrieved from BM25 & Vector
    RRF_K: int = 60                  # Smoothing constant for Reciprocal Rank Fusion
    
    # Valkey / Redis Configuration
    VALKEY_HOST: str = os.getenv("VALKEY_HOST", "127.0.0.1")
    VALKEY_PORT: int = int(os.getenv("VALKEY_PORT", "6379"))
    VALKEY_DB: int = int(os.getenv("VALKEY_DB", "0"))
    VALKEY_PASSWORD: str = os.getenv("VALKEY_PASSWORD", "")
    
    # Safety & Directory Restrictions
    ALLOWED_PROJECT_DIR: str = "/L9/nagul/himes-ai"
    
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        extra="ignore"
    )

settings = RAGSettings()
