"""
Retriever for external knowledge outside Wittgenstein's time.
Used to provide factual context for modern concepts and topics.
"""

from typing import List, Tuple, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_faiss_index, search_faiss_index
from config import Config


class ExternalKnowledgeRetriever:
    """
    Retriever for external knowledge outside Wittgenstein's time.
    This retriever provides factual context for modern concepts,
    technologies, and topics that Wittgenstein could not have known about.
    """

    def __init__(self):
        """Initialize the external knowledge retriever."""
        self.index = None
        self.metadata = None
        self.load_index()

    def load_index(self):
        """Load the FAISS index for external knowledge."""
        self.index, self.metadata = load_faiss_index(Config.EXTERNAL_INDEX_PATH)
        if self.index is None:
            print(
                "Warning: No external knowledge index found. Run data ingestion first."
            )

    def retrieve(
        self, query: str, top_k: int = None
    ) -> List[Tuple[float, Dict[str, Any]]]:
        """
        Retrieve relevant external knowledge for the given query.

        Args:
            query: The search query
            top_k: Number of results to return (defaults to config setting)

        Returns:
            List of (score, metadata) tuples
        """
        if top_k is None:
            top_k = Config.TOP_K_EXTERNAL

        if self.index is None or self.metadata is None:
            return []

        results = search_faiss_index(
            query=query,
            index=self.index,
            metadata=self.metadata,
            top_k=top_k,
            embedding_model=Config.EMBEDDING_MODEL,
        )

        return results

    def get_factual_context(self, query: str) -> str:
        """
        Get factual context from external knowledge for the given query.

        Args:
            query: The search query

        Returns:
            Formatted string with factual context
        """
        results = self.retrieve(query)

        if not results:
            return "No external factual context found."

        context_text = "External factual context (not to be quoted directly):\n\n"
        for i, (score, metadata) in enumerate(results, 1):
            content = metadata.get("content", "No content available")
            source = metadata.get("source", "Unknown source")
            context_text += f"{i}. [{source}] {content}\n\n"

        return context_text

    def is_available(self) -> bool:
        """Check if the external knowledge index is available."""
        return self.index is not None and self.metadata is not None
