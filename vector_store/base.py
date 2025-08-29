from __future__ import annotations

"""Abstract base class for vector stores.

Defines the minimal API required for indexing and querying vectors.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple


class VectorStore(ABC):
    """Interface for vector storage backends."""

    @abstractmethod
    def index_embedding(
        self, identifier: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Index a single embedding.

        Parameters
        ----------
        identifier:
            Unique identifier for the vector.
        vector:
            Embedding values.
        metadata:
            Optional associated metadata.
        """

    @abstractmethod
    def query_embedding(
        self, vector: List[float], top_k: int = 5
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Query the most similar embeddings.

        Returns a list of tuples ``(id, score, metadata)``.
        """
