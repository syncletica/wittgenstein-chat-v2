#!/usr/bin/env python3
"""
Wittgenstein Chatbot - Main Application
A terminal-based chatbot that role-plays as Ludwig Wittgenstein using RAG.
"""

import os
import sys
from typing import List, Dict
from langchain_openai import ChatOpenAI
from prompt_builder import PromptBuilder
from config import Config

# Enable LangSmith tracing if API key is present
if Config.LANGSMITH_API_KEY:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = Config.LANGSMITH_PROJECT
    os.environ["LANGCHAIN_API_KEY"] = Config.LANGSMITH_API_KEY


class WittgensteinChatbot:
    """
    Main chatbot class that orchestrates the conversation.
    """

    def __init__(self):
        """Initialize the Wittgenstein chatbot."""
        # Validate configuration
        Config.validate()

        # Initialize components
        self.prompt_builder = PromptBuilder()
        self.llm = ChatOpenAI(
            model=Config.OPENAI_MODEL,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
            openai_api_key=Config.OPENAI_API_KEY,
        )

        # Conversation history
        self.conversation_history: List[Dict] = []

        # Check retriever availability
        self._check_retrievers()

    def _check_retrievers(self):
        """Check and report the status of all retrievers."""
        available = self.prompt_builder.get_available_retrievers()

        print("Retriever Status:")
        for name, status in available.items():
            status_str = "✓ Available" if status else "✗ Not available"
            print(f"  {name.capitalize()}: {status_str}")

        if not any(available.values()):
            print(
                "\nWarning: No retrievers are available. Consider running data ingestion first."
            )
            print(
                'Run: python -c "from loaders.ingest import DataIngester; DataIngester().create_sample_data(); DataIngester().ingest_all()"'
            )

    def chat(self):
        """Start the interactive chat session."""
        print("=" * 60)
        print("WITTGENSTEIN CHATBOT")
        print("=" * 60)
        print("You are now conversing with Ludwig Wittgenstein.")
        print("Type 'quit', 'exit', or 'bye' to end the conversation.")
        print("Type 'help' for available commands.")
        print("=" * 60)
        print()

        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                # Check for exit commands
                if user_input.lower() in ["quit", "exit", "bye"]:
                    print(
                        "\nWittgenstein: Goodbye. Remember, 'Whereof one cannot speak, thereof one must be silent.'"
                    )
                    break

                # Check for help command
                if user_input.lower() == "help":
                    self._show_help()
                    continue

                # Check for clear command
                if user_input.lower() == "clear":
                    self.conversation_history.clear()
                    print("Conversation history cleared.")
                    continue

                # Check for status command
                if user_input.lower() == "status":
                    self._show_status()
                    continue

                # Skip empty input
                if not user_input:
                    continue

                # Process the query
                response = self._process_query(user_input)

                # Display response
                print(f"\nWittgenstein: {response}\n")

                # Update conversation history
                self.conversation_history.append(
                    {"role": "user", "content": user_input}
                )
                self.conversation_history.append(
                    {"role": "assistant", "content": response}
                )

                # Limit history size
                if len(self.conversation_history) > Config.MAX_HISTORY * 2:
                    self.conversation_history = self.conversation_history[
                        -Config.MAX_HISTORY * 2 :
                    ]

            except KeyboardInterrupt:
                print(
                    "\n\nWittgenstein: The conversation has been interrupted. Farewell."
                )
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again or type 'help' for assistance.")

    def _process_query(self, user_query: str) -> str:
        """
        Process a user query and generate a response.

        Args:
            user_query: The user's input

        Returns:
            Wittgenstein's response
        """
        try:
            # Build the prompt
            prompt = self.prompt_builder.build_prompt(
                user_query, self.conversation_history
            )

            # Get response from OpenAI
            response = self.llm.invoke(prompt)

            # Extract the content
            if hasattr(response, "content"):
                return response.content
            else:
                return str(response)

        except Exception as e:
            return f"I find myself unable to respond properly at the moment. The error is: {str(e)}"

    def _show_help(self):
        """Show help information."""
        help_text = """
Available Commands:
  help     - Show this help message
  clear    - Clear conversation history
  status   - Show retriever status
  quit     - Exit the chatbot
  exit     - Exit the chatbot
  bye      - Exit the chatbot

You can ask me about:
  - Philosophy and language
  - Logic and mathematics
  - The nature of reality
  - Modern concepts (I'll approach them philosophically)
  - Any topic that interests you philosophically

I will respond as Wittgenstein would, drawing from my writings and philosophical approach.
"""
        print(help_text)

    def _show_status(self):
        """Show the current status of retrievers."""
        available = self.prompt_builder.get_available_retrievers()

        print("\nCurrent Status:")
        print("=" * 30)
        for name, status in available.items():
            status_str = "✓ Available" if status else "✗ Not available"
            print(f"{name.capitalize()}: {status_str}")

        print(f"Conversation History: {len(self.conversation_history)} turns")
        print("=" * 30)


def main():
    """Main entry point for the application."""
    try:
        # Check if OpenAI API key is set
        if not Config.OPENAI_API_KEY:
            print("Error: OPENAI_API_KEY environment variable is required.")
            print("Please set your OpenAI API key:")
            print("export OPENAI_API_KEY='your-api-key-here'")
            print("Or create a .env file with: OPENAI_API_KEY=your-api-key-here")
            return

        # Create and start the chatbot
        chatbot = WittgensteinChatbot()
        chatbot.chat()

    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check your configuration and try again.")


if __name__ == "__main__":
    main()
