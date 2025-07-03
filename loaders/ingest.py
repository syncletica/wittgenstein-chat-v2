"""
Data ingestion module for the Wittgenstein chatbot.
Handles loading, processing, and indexing of text data.
"""

import os
import json
from typing import List, Dict, Any
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_text_files, split_texts, create_faiss_index
from config import Config


class DataIngester:
    """
    Data ingester for processing and indexing text data.
    Handles the creation of FAISS indexes from text files.
    """

    def __init__(self):
        """Initialize the data ingester."""
        self.config = Config

    def ingest_authored_texts(self):
        """
        Ingest Wittgenstein's authored texts.
        Creates FAISS index for style and philosophical approach.
        """
        print("Ingesting authored texts...")

        # Load text files
        texts = load_text_files(self.config.AUTHORED_DATA_PATH)

        if not texts:
            print(f"No text files found in {self.config.AUTHORED_DATA_PATH}")
            return

        # Split texts into chunks
        documents = split_texts(
            texts=texts,
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP,
        )

        # Add metadata
        for doc in documents:
            doc.metadata = {
                "content": doc.page_content,
                "type": "authored",
                "source": "wittgenstein_writings",
            }

        # Create FAISS index
        create_faiss_index(
            documents=documents,
            index_path=self.config.AUTHORED_INDEX_PATH,
            embedding_model=self.config.EMBEDDING_MODEL,
        )

        print(f"Ingested {len(documents)} authored text chunks")

    def ingest_descriptive_sources(self):
        """
        Ingest descriptive sources about Wittgenstein's thought.
        Creates FAISS index for philosophical context.
        """
        print("Ingesting descriptive sources...")

        # Load text files
        texts = load_text_files(self.config.DESCRIPTIVE_DATA_PATH)

        if not texts:
            print(f"No text files found in {self.config.DESCRIPTIVE_DATA_PATH}")
            return

        # Split texts into chunks
        documents = split_texts(
            texts=texts,
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP,
        )

        # Add metadata
        for doc in documents:
            doc.metadata = {
                "content": doc.page_content,
                "type": "descriptive",
                "source": "secondary_sources",
            }

        # Create FAISS index
        create_faiss_index(
            documents=documents,
            index_path=self.config.DESCRIPTIVE_INDEX_PATH,
            embedding_model=self.config.EMBEDDING_MODEL,
        )

        print(f"Ingested {len(documents)} descriptive source chunks")

    def ingest_external_knowledge(self):
        """
        Ingest external knowledge outside Wittgenstein's time.
        Creates FAISS index for factual context.
        """
        print("Ingesting external knowledge...")

        # Load text files
        texts = load_text_files(self.config.EXTERNAL_DATA_PATH)

        if not texts:
            print(f"No text files found in {self.config.EXTERNAL_DATA_PATH}")
            return

        # Split texts into chunks
        documents = split_texts(
            texts=texts,
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP,
        )

        # Add metadata
        for doc in documents:
            doc.metadata = {
                "content": doc.page_content,
                "type": "external",
                "source": "modern_knowledge",
            }

        # Create FAISS index
        create_faiss_index(
            documents=documents,
            index_path=self.config.EXTERNAL_INDEX_PATH,
            embedding_model=self.config.EMBEDDING_MODEL,
        )

        print(f"Ingested {len(documents)} external knowledge chunks")

    def ingest_all(self):
        """
        Ingest all data types.
        Creates all three FAISS indexes.
        """
        print("Starting data ingestion...")

        # Validate configuration
        self.config.validate()

        # Ingest each data type
        self.ingest_authored_texts()
        self.ingest_descriptive_sources()
        self.ingest_external_knowledge()

        print("Data ingestion complete!")

    def create_sample_data(self):
        """
        Create sample data files for testing.
        This creates minimal example data in the data directories.
        """
        print("Creating sample data...")

        # Sample authored texts
        authored_samples = [
            {
                "filename": "tractatus_excerpt.txt",
                "content": """1. The world is all that is the case.
1.1 The world is the totality of facts, not of things.
1.11 The world is determined by the facts, and by these being all the facts.
1.12 For the totality of facts determines both what is the case, and also all that is not the case.
1.13 The facts in logical space are the world.
1.2 The world divides into facts.
1.21 Any one can either be the case or not be the case, and everything else remain the same.""",
            },
            {
                "filename": "philosophical_investigations_excerpt.txt",
                "content": """1. "Cum ipsi (majores homines) appellabant rem aliquam, et cum secundum eam vocem corpus ad aliquid movebant, videbam, et tenebam hoc ab eis vocari rem illam, quod sonabant, cum eam vellent ostendere. Hoc autem eos velle ex motu corporis aperiebatur: tamquam verbis naturalibus omnium gentium, quae fiunt vultu et nutu oculorum, ceterorumque membrorum actu, et sonitu vocis indicante affectionem animi in petendis, habendis, rejiciendis, fugiendisve rebus. Ita verba in variis sententiis locis suis posita, et crebro audita, quarum rerum signa essent, paulatim colligebam, measque jam voluntates, edomito in eis signis ore, per haec enuntiabam." (Augustine, Confessions, I. 8.)""",
            },
        ]

        # Sample descriptive sources
        descriptive_samples = [
            {
                "filename": "wittgenstein_biography.txt",
                "content": """Ludwig Wittgenstein (1889-1951) was an Austrian-British philosopher who worked primarily in logic, the philosophy of mathematics, the philosophy of mind, and the philosophy of language. He is considered one of the most important philosophers of the 20th century. His early work, the Tractatus Logico-Philosophicus, influenced the logical positivism of the Vienna Circle, while his later work, the Philosophical Investigations, was a major influence on ordinary language philosophy and post-analytic philosophy.""",
            },
            {
                "filename": "language_games_explanation.txt",
                "content": """Wittgenstein's concept of language games suggests that the meaning of words is determined by their use in specific contexts or 'forms of life.' Language is not a static system but a dynamic activity embedded in human practices. Different language games have different rules, and understanding a word requires understanding the game in which it is played. This view challenges the idea that language has a single, fixed meaning and emphasizes the contextual nature of linguistic understanding.""",
            },
        ]

        # Sample external knowledge
        external_samples = [
            {
                "filename": "artificial_intelligence.txt",
                "content": """Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans. The term was coined in 1956 at the Dartmouth Conference. AI encompasses various subfields including machine learning, natural language processing, computer vision, and robotics. Modern AI systems can perform tasks such as image recognition, language translation, and decision-making that typically require human intelligence.""",
            },
            {
                "filename": "quantum_computing.txt",
                "content": """Quantum computing is a type of computation that harnesses the collective properties of quantum states to perform calculations. Unlike classical computers that use bits (0 or 1), quantum computers use quantum bits or qubits that can exist in multiple states simultaneously through superposition. This allows quantum computers to solve certain problems much faster than classical computers, particularly in areas like cryptography, optimization, and simulation.""",
            },
        ]

        # Create directories and write sample files
        for sample_data, directory in [
            (authored_samples, self.config.AUTHORED_DATA_PATH),
            (descriptive_samples, self.config.DESCRIPTIVE_DATA_PATH),
            (external_samples, self.config.EXTERNAL_DATA_PATH),
        ]:
            os.makedirs(directory, exist_ok=True)

            for sample in sample_data:
                filepath = os.path.join(directory, sample["filename"])
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(sample["content"])

        print("Sample data created successfully!")
        print(f"Created {len(authored_samples)} authored text samples")
        print(f"Created {len(descriptive_samples)} descriptive source samples")
        print(f"Created {len(external_samples)} external knowledge samples")
