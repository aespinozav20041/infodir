"""Vector store factory and exports."""

from .base import VectorStore
from .milvus_store import MilvusVectorStore
from .weaviate_store import WeaviateVectorStore
from .pgvector_store import PGVectorStore


def get_vector_store(kind: str, **kwargs) -> VectorStore:
    """Factory for vector store implementations."""
    kind = kind.lower()
    if kind == "milvus":
        return MilvusVectorStore(**kwargs)
    if kind == "weaviate":
        return WeaviateVectorStore(**kwargs)
    if kind in {"pgvector", "postgres"}:
        return PGVectorStore(**kwargs)
    raise ValueError(f"Unknown vector store kind: {kind}")

__all__ = [
    "VectorStore",
    "MilvusVectorStore",
    "WeaviateVectorStore",
    "PGVectorStore",
    "get_vector_store",
]
