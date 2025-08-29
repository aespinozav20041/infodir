"""Weaviate implementation of :class:`VectorStore`."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import weaviate

from .base import VectorStore


class WeaviateVectorStore(VectorStore):
    """Store backed by a Weaviate instance."""

    def __init__(self, url: str = "http://localhost:8080", class_name: str = "Document"):
        self.client = weaviate.Client(url)
        self.class_name = class_name
        if not self.client.schema.contains({"class": class_name}):
            class_obj = {
                "class": class_name,
                "vectorizer": "none",
                "properties": [
                    {"name": "content", "dataType": ["text"]},
                ],
            }
            self.client.schema.create_class(class_obj)

    def index_embedding(
        self, identifier: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        data = metadata or {}
        data["id"] = identifier
        self.client.data_object.create(data, class_name=self.class_name, vector=vector)

    def query_embedding(
        self, vector: List[float], top_k: int = 5
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        result = (
            self.client.query.get(self.class_name, ["content"])
            .with_near_vector({"vector": vector})
            .with_limit(top_k)
            .with_additional(["id", "distance"])
            .do()
        )
        hits = []
        for obj in result.get("data", {}).get("Get", {}).get(self.class_name, []):
            hits.append(
                (
                    obj["_additional"]["id"],
                    float(obj["_additional"]["distance"]),
                    {"content": obj.get("content")},
                )
            )
        return hits
