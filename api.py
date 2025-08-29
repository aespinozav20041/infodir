"""Simple API exposing indexing and querying endpoints."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from vector_store import VectorStore, get_vector_store

STORE_KIND = os.getenv("VECTOR_STORE", "weaviate")
store: VectorStore = get_vector_store(STORE_KIND)

app = FastAPI()


class IndexRequest(BaseModel):
    id: str
    vector: List[float]
    metadata: Optional[Dict[str, Any]] = None


class QueryRequest(BaseModel):
    vector: List[float]
    top_k: int = 5


@app.post("/index")
def index(req: IndexRequest) -> Dict[str, str]:
    store.index_embedding(req.id, req.vector, req.metadata)
    return {"status": "ok"}


@app.post("/query")
def query(req: QueryRequest) -> Dict[str, Any]:
    results = store.query_embedding(req.vector, req.top_k)
    return {
        "results": [
            {"id": ident, "score": score, "metadata": meta} for ident, score, meta in results
        ]
    }
