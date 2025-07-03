"""
Configuration settings for the Wittgenstein Chatbot.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for the Wittgenstein chatbot."""

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4"  # or "gpt-3.5-turbo" for faster/cheaper responses

    # FAISS Index Configuration
    FAISS_INDEX_PATH = "indexes"
    AUTHORED_INDEX_PATH = os.path.join(FAISS_INDEX_PATH, "faiss_authored")
    DESCRIPTIVE_INDEX_PATH = os.path.join(FAISS_INDEX_PATH, "faiss_descriptive")
    EXTERNAL_INDEX_PATH = os.path.join(FAISS_INDEX_PATH, "faiss_external")

    # Data Paths
    DATA_PATH = "data"
    AUTHORED_DATA_PATH = os.path.join(DATA_PATH, "authored_texts")
    DESCRIPTIVE_DATA_PATH = os.path.join(DATA_PATH, "descriptive_sources")
    EXTERNAL_DATA_PATH = os.path.join(DATA_PATH, "external_knowledge")

    # Retrieval Configuration
    TOP_K_AUTHORED = 3  # Number of authored text chunks to retrieve
    TOP_K_DESCRIPTIVE = 2  # Number of descriptive source chunks to retrieve
    TOP_K_EXTERNAL = 2  # Number of external knowledge chunks to retrieve

    # Embedding Configuration
    EMBEDDING_MODEL = "text-embedding-ada-002"
    CHUNK_SIZE = 1000  # Size of text chunks for embedding
    CHUNK_OVERLAP = 200  # Overlap between chunks

    # Prompt Configuration
    MAX_TOKENS = 2000  # Maximum tokens for OpenAI response
    TEMPERATURE = 0.7  # Creativity level (0.0 = deterministic, 1.0 = very creative)

    # Chat Configuration
    MAX_HISTORY = 5  # Maximum conversation turns to remember

    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # Create directories if they don't exist
        os.makedirs(cls.FAISS_INDEX_PATH, exist_ok=True)
        os.makedirs(cls.AUTHORED_DATA_PATH, exist_ok=True)
        os.makedirs(cls.DESCRIPTIVE_DATA_PATH, exist_ok=True)
        os.makedirs(cls.EXTERNAL_DATA_PATH, exist_ok=True)
