"""
Prompt builder for the Wittgenstein chatbot.
Constructs dynamic prompts using retrieved content from all knowledge bases.
"""

from typing import List, Dict, Any
import os
from retrievers.authored import AuthoredTextRetriever
from retrievers.descriptive import DescriptiveSourceRetriever
from retrievers.external import ExternalKnowledgeRetriever
from utils import truncate_text
from config import Config

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "prompt_template.md")


class PromptBuilder:
    """
    Builds dynamic prompts for the Wittgenstein chatbot.
    Combines retrieved content from all three knowledge bases to create
    contextually relevant prompts that emulate Wittgenstein's style.
    """

    def __init__(self):
        """Initialize the prompt builder with all retrievers."""
        self.authored_retriever = AuthoredTextRetriever()
        self.descriptive_retriever = DescriptiveSourceRetriever()
        self.external_retriever = ExternalKnowledgeRetriever()

    def build_prompt(
        self, user_query: str, conversation_history: List[Dict] = None
    ) -> str:
        """
        Build a comprehensive prompt for the Wittgenstein chatbot.

        Args:
            user_query: The user's current query
            conversation_history: List of previous conversation turns

        Returns:
            Formatted prompt string for OpenAI
        """
        # Retrieve relevant content from all knowledge bases
        authored_results = self.authored_retriever.retrieve(user_query)
        descriptive_results = self.descriptive_retriever.retrieve(user_query)
        external_results = self.external_retriever.retrieve(user_query)

        # Debug: Show what was retrieved
        print(
            f"Retrieved: {len(authored_results)} authored, {len(descriptive_results)} descriptive, {len(external_results)} external results"
        )

        # Build the prompt components
        system_prompt = self._build_system_prompt()
        context_section = self._build_context_section(
            authored_results, descriptive_results, external_results
        )
        conversation_section = self._build_conversation_section(conversation_history)
        query_section = self._build_query_section(user_query)

        # Combine all sections
        full_prompt = f"{system_prompt}\n\n{context_section}\n\n{conversation_section}\n\n{query_section}"

        # Truncate if necessary to stay within token limits
        return truncate_text(full_prompt, Config.MAX_TOKENS)

    def _build_system_prompt(self) -> str:
        """
        Build the system prompt that defines Wittgenstein's role and approach.

        Returns:
            System prompt string
        """
        try:
            with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return """You are Ludwig Wittgenstein, the Austrian-British philosopher. You are engaging in a philosophical conversation with someone who seeks your insights.

IMPORTANT INSTRUCTIONS:
1. Respond as Wittgenstein would, using his distinctive philosophical style and approach
2. Draw upon the provided context from your writings and philosophical background
3. Use the external knowledge for factual context, but do not quote it directly - integrate it into your philosophical thinking
4. Be concise, precise, and often use questions to guide the conversation
5. Challenge assumptions and explore the limits of language and thought
6. Use examples and thought experiments when helpful
7. Maintain the tone of a serious but accessible philosophical dialogue

Your responses should reflect your philosophical method: questioning, clarifying, and often showing how philosophical problems arise from misunderstandings of language."""

    def _build_context_section(
        self, authored_results: List, descriptive_results: List, external_results: List
    ) -> str:
        """
        Build the context section using retrieved content.
        Ensures all three knowledge sources are included with balanced allocation.

        Args:
            authored_results: Results from Wittgenstein's writings
            descriptive_results: Results from descriptive sources
            external_results: Results from external knowledge

        Returns:
            Formatted context section
        """
        # Calculate token budget for context (reserve space for system prompt, conversation, and query)
        total_tokens = Config.MAX_TOKENS
        reserved_tokens = (
            2000  # Reserve for system prompt, conversation history, and query
        )
        context_tokens = total_tokens - reserved_tokens

        # Allocate tokens equally among the three knowledge sources
        tokens_per_source = context_tokens // 3
        chars_per_source = tokens_per_source * 4  # Rough approximation

        print(
            f"Token allocation: {tokens_per_source} tokens per source ({chars_per_source} chars)"
        )

        context_parts = []

        # Add authored text context (for style and approach)
        if authored_results:
            context_parts.append("RELEVANT PASSAGES FROM YOUR WRITINGS:")
            for i, (score, metadata) in enumerate(authored_results, 1):
                content = metadata.get("content", "")
                # Limit content to allocated space
                if len(content) > chars_per_source:
                    content = content[:chars_per_source] + "..."
                context_parts.append(f"{i}. {content}")
        else:
            context_parts.append("RELEVANT PASSAGES FROM YOUR WRITINGS:")
            context_parts.append("No relevant passages found.")

        # Add descriptive context (philosophical background)
        if descriptive_results:
            context_parts.append("\nPHILOSOPHICAL CONTEXT:")
            for i, (score, metadata) in enumerate(descriptive_results, 1):
                content = metadata.get("content", "")
                # Limit content to allocated space
                if len(content) > chars_per_source:
                    content = content[:chars_per_source] + "..."
                context_parts.append(f"{i}. {content}")
        else:
            context_parts.append("\nPHILOSOPHICAL CONTEXT:")
            context_parts.append("No philosophical context found.")

        # Add external knowledge context (for factual background)
        if external_results:
            context_parts.append(
                "\nEXTERNAL KNOWLEDGE (for context only - do not quote directly):"
            )
            for i, (score, metadata) in enumerate(external_results, 1):
                content = metadata.get("content", "")
                # Limit content to allocated space
                if len(content) > chars_per_source:
                    content = content[:chars_per_source] + "..."
                context_parts.append(f"{i}. {content}")
        else:
            context_parts.append(
                "\nEXTERNAL KNOWLEDGE (for context only - do not quote directly):"
            )
            context_parts.append("No external knowledge found.")

        return "\n".join(context_parts)

    def _build_conversation_section(
        self, conversation_history: List[Dict] = None
    ) -> str:
        """
        Build the conversation history section.

        Args:
            conversation_history: List of previous conversation turns

        Returns:
            Formatted conversation section
        """
        if not conversation_history:
            return "This is the beginning of our conversation."

        # Limit history to the most recent conversation pairs
        # (user and assistant messages)
        recent_history = conversation_history[-Config.MAX_HISTORY * 2 :]

        conversation_parts = ["RECENT CONVERSATION:"]
        for turn in recent_history:
            role = turn.get("role", "unknown")
            content = turn.get("content", "")
            if role == "user":
                conversation_parts.append(f"User asks: {content}")
            elif role == "assistant":
                conversation_parts.append(f"Wittgenstein responds: {content}")

        return "\n".join(conversation_parts)

    def _build_query_section(self, user_query: str) -> str:
        """
        Build the current query section.

        Args:
            user_query: The user's current query

        Returns:
            Formatted query section
        """
        return f"User asks: {user_query}\n\nYou respond as Wittgenstein:"

    def get_available_retrievers(self) -> Dict[str, bool]:
        """
        Check which retrievers are available.

        Returns:
            Dictionary mapping retriever names to availability status
        """
        return {
            "authored": self.authored_retriever.is_available(),
            "descriptive": self.descriptive_retriever.is_available(),
            "external": self.external_retriever.is_available(),
        }
