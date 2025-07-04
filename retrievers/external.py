"""
Retriever for external knowledge outside Wittgenstein's time.
Used to provide factual context for modern concepts and topics.
"""

from typing import List, Tuple, Dict, Any

from config import Config
from .base import BaseRetriever


class ExternalKnowledgeRetriever(BaseRetriever):
    """
    Retriever for external knowledge outside Wittgenstein's time.
    This retriever provides factual context for modern concepts,
    technologies, and topics that Wittgenstein could not have known about.
    """

    def __init__(self):
        """Initialize the external knowledge retriever."""
        super().__init__(
            index_path=Config.EXTERNAL_INDEX_PATH,
            default_top_k=Config.TOP_K_EXTERNAL,
        )


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


