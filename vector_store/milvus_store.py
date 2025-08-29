"""Milvus implementation of :class:`VectorStore`."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple

from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections

from .base import VectorStore


class MilvusVectorStore(VectorStore):
    """Store backed by a Milvus collection.

    Parameters
    ----------
    host, port:
        Milvus connection parameters.
    collection:
        Collection name to use.
    dim:
        Dimensionality of the embeddings.
    """

    def __init__(self, host: str = "localhost", port: str = "19530", collection: str = "embeddings", dim: int = 768):
        connections.connect(host=host, port=port)
        self.collection_name = collection
        self.dim = dim
        if collection not in connections.get_connection().list_collections():
            fields = [
                FieldSchema(name="id", dtype=DataType.VARCHAR, is_primary=True, max_length=64),
                FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
                FieldSchema(name="metadata", dtype=DataType.JSON, default={}),
            ]
            schema = CollectionSchema(fields, description="vector store")
            self.collection = Collection(name=collection, schema=schema)
            self.collection.create_index("vector", {"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 1024}})
        else:
            self.collection = Collection(collection)

    def index_embedding(
        self, identifier: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        data = [[identifier], [vector], [metadata or {}]]
        self.collection.insert(data)
        self.collection.flush()

    def query_embedding(
        self, vector: List[float], top_k: int = 5
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = self.collection.search([vector], "vector", search_params, top_k=top_k, output_fields=["metadata"])
        out: List[Tuple[str, float, Dict[str, Any]]] = []
        for hit in results[0]:
            out.append((hit.id, float(hit.distance), json.loads(hit.entity.get("metadata", {}))))
        return out
