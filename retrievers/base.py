"""Base retriever class for FAISS-backed indexes."""

from typing import List, Tuple, Dict, Any

from config import Config
from utils import load_faiss_index, search_faiss_index


class BaseRetriever:
    """Generic retriever for FAISS indexes."""

    def __init__(self, index_path: str, default_top_k: int):
        self.index_path = index_path
        self.default_top_k = default_top_k
        self.index = None
        self.metadata = None
        self.load_index()

    def load_index(self) -> None:
        """Load the FAISS index and metadata."""
        self.index, self.metadata = load_faiss_index(self.index_path)
        if self.index is None:
            print(f"Warning: No index found at {self.index_path}. Run data ingestion first.")

    def retrieve(self, query: str, top_k: int | None = None) -> List[Tuple[float, Dict[str, Any]]]:
        """Retrieve relevant entries for a query."""
        if top_k is None:
            top_k = self.default_top_k
        if self.index is None or self.metadata is None:
            return []
        return search_faiss_index(
            query=query,
            index=self.index,
            metadata=self.metadata,
            top_k=top_k,
            embedding_model=Config.EMBEDDING_MODEL,
        )

    def is_available(self) -> bool:
        """Return True if the retriever index is available."""
        return self.index is not None and self.metadata is not None
