"""
Retriever for Wittgenstein's authored texts.
Used to determine response style and philosophical approach.
"""

from typing import List, Tuple, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_faiss_index, search_faiss_index
from config import Config


class AuthoredTextRetriever:
    """
    Retriever for Wittgenstein's own writings.
    This retriever is used to find passages from Wittgenstein's works
    that can inform the style and philosophical approach of responses.
    """

    def __init__(self):
        """Initialize the authored text retriever."""
        self.index = None
        self.metadata = None
        self.load_index()

    def load_index(self):
        """Load the FAISS index for authored texts."""
        self.index, self.metadata = load_faiss_index(Config.AUTHORED_INDEX_PATH)
        if self.index is None:
            print("Warning: No authored text index found. Run data ingestion first.")

    def retrieve(
        self, query: str, top_k: int = None
    ) -> List[Tuple[float, Dict[str, Any]]]:
        """
        Retrieve relevant passages from Wittgenstein's writings.

        Args:
            query: The search query
            top_k: Number of results to return (defaults to config setting)

        Returns:
            List of (score, metadata) tuples
        """
        if top_k is None:
            top_k = Config.TOP_K_AUTHORED

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

    def get_style_examples(self, query: str) -> str:
        """
        Get style examples from Wittgenstein's writings for the given query.

        Args:
            query: The search query

        Returns:
            Formatted string with style examples
        """
        results = self.retrieve(query)

        if not results:
            return "No style examples found."

        style_text = "Style examples from Wittgenstein's writings:\n\n"
        for i, (score, metadata) in enumerate(results, 1):
            content = metadata.get("content", "No content available")
            style_text += f"{i}. {content}\n\n"

        return style_text

    def is_available(self) -> bool:
        """Check if the authored text index is available."""
        return self.index is not None and self.metadata is not None
