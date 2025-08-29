"""PostgreSQL + pgvector implementation of :class:`VectorStore`."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extras import Json

from .base import VectorStore


class PGVectorStore(VectorStore):
    """Store backed by PostgreSQL with the pgvector extension."""

    def __init__(self, dsn: str, table: str = "embeddings", dim: int = 768):
        self.conn = psycopg2.connect(dsn)
        self.table = table
        self.dim = dim
        with self.conn, self.conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id TEXT PRIMARY KEY,
                    embedding VECTOR({dim}),
                    metadata JSONB
                )
                """
            )
            cur.execute(
                f"""
                CREATE INDEX IF NOT EXISTS {table}_embedding_idx
                ON {table} USING ivfflat (embedding vector_l2_ops)
                WITH (lists = 100)
                """
            )

    def index_embedding(
        self, identifier: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        with self.conn, self.conn.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO {self.table} (id, embedding, metadata)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO UPDATE
                SET embedding = EXCLUDED.embedding,
                    metadata = EXCLUDED.metadata
                """,
                (identifier, vector, Json(metadata or {})),
            )

    def query_embedding(
        self, vector: List[float], top_k: int = 5
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT id, embedding <-> %s AS distance, metadata FROM {self.table} ORDER BY distance LIMIT %s",
                (vector, top_k),
            )
            return [(row[0], float(row[1]), row[2] or {}) for row in cur.fetchall()]
