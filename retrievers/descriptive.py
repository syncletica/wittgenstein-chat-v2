"""
Retriever for descriptive sources about Wittgenstein's thought.
Used to provide philosophical context and interpretation.
"""

from typing import List, Tuple, Dict, Any

from config import Config
from .base import BaseRetriever


class DescriptiveSourceRetriever(BaseRetriever):
    """
    Retriever for descriptive sources about Wittgenstein's thought.
    This retriever provides philosophical context and interpretation
    from secondary sources and commentaries.
    """

    def __init__(self):
        """Initialize the descriptive source retriever."""
        super().__init__(
            index_path=Config.DESCRIPTIVE_INDEX_PATH,
            default_top_k=Config.TOP_K_DESCRIPTIVE,
        )


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


