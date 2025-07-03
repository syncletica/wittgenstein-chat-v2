"""
Retriever for descriptive sources about Wittgenstein's thought.
Used to provide philosophical context and interpretation.
"""

from typing import List, Tuple, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_faiss_index, search_faiss_index
from config import Config


class DescriptiveSourceRetriever:
    """
    Retriever for descriptive sources about Wittgenstein's thought.
    This retriever provides philosophical context and interpretation
    from secondary sources and commentaries.
    """

    def __init__(self):
        """Initialize the descriptive source retriever."""
        self.index = None
        self.metadata = None
        self.load_index()

    def load_index(self):
        """Load the FAISS index for descriptive sources."""
        self.index, self.metadata = load_faiss_index(Config.DESCRIPTIVE_INDEX_PATH)
        if self.index is None:
            print(
                "Warning: No descriptive source index found. Run data ingestion first."
            )

    def retrieve(
        self, query: str, top_k: int = None
    ) -> List[Tuple[float, Dict[str, Any]]]:
        """
        Retrieve relevant descriptive sources about Wittgenstein's thought.

        Args:
            query: The search query
            top_k: Number of results to return (defaults to config setting)

        Returns:
            List of (score, metadata) tuples
        """
        if top_k is None:
            top_k = Config.TOP_K_DESCRIPTIVE

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

    def get_philosophical_context(self, query: str) -> str:
        """
        Get philosophical context from descriptive sources for the given query.

        Args:
            query: The search query

        Returns:
            Formatted string with philosophical context
        """
        results = self.retrieve(query)

        if not results:
            return "No philosophical context found."

        context_text = "Philosophical context and interpretation:\n\n"
        for i, (score, metadata) in enumerate(results, 1):
            content = metadata.get("content", "No content available")
            source = metadata.get("source", "Unknown source")
            context_text += f"{i}. [{source}] {content}\n\n"

        return context_text

    def is_available(self) -> bool:
        """Check if the descriptive source index is available."""
        return self.index is not None and self.metadata is not None
