"""
Retriever for Wittgenstein's authored texts.
Used to determine response style and philosophical approach.
"""

from typing import List, Tuple, Dict, Any

from config import Config
from .base import BaseRetriever


class AuthoredTextRetriever(BaseRetriever):
    """
    Retriever for Wittgenstein's own writings.
    This retriever is used to find passages from Wittgenstein's works
    that can inform the style and philosophical approach of responses.
    """

    def __init__(self):
        """Initialize the authored text retriever."""
        super().__init__(
            index_path=Config.AUTHORED_INDEX_PATH,
            default_top_k=Config.TOP_K_AUTHORED,
        )


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


