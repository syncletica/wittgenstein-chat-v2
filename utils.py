"""
Utility functions for the Wittgenstein chatbot.
"""

import os
import json
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
import faiss
import numpy as np


def load_text_files(directory: str) -> List[str]:
    """
    Load all text files from a directory.

    Args:
        directory: Path to directory containing text files

    Returns:
        List of text content from all files
    """
    texts = []
    if not os.path.exists(directory):
        return texts

    for filename in os.listdir(directory):
        if filename.endswith((".txt", ".md")):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    texts.append(f.read())
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

    return texts


def split_texts(
    texts: List[str], chunk_size: int = 1000, chunk_overlap: int = 200
) -> List[Document]:
    """
    Split texts into chunks for embedding.

    Args:
        texts: List of text strings
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks

    Returns:
        List of Document objects
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    documents = []
    for text in texts:
        chunks = text_splitter.split_text(text)
        for chunk in chunks:
            documents.append(Document(page_content=chunk))

    return documents


def create_faiss_index(
    documents: List[Document],
    index_path: str,
    embedding_model: str = "text-embedding-ada-002",
):
    """
    Create a FAISS index from documents.

    Args:
        documents: List of Document objects
        index_path: Path to save the FAISS index
        embedding_model: OpenAI embedding model to use
    """
    if not documents:
        print(f"No documents to index for {index_path}")
        return

    # Initialize embeddings
    embeddings = OpenAIEmbeddings(model=embedding_model)

    # Get embeddings for all documents
    texts = [doc.page_content for doc in documents]
    embedding_vectors = embeddings.embed_documents(texts)

    # Convert to numpy array
    embedding_vectors = np.array(embedding_vectors).astype("float32")

    # Create FAISS index
    dimension = embedding_vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embedding_vectors)

    # Save index and documents
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, f"{index_path}.faiss")

    # Save document metadata
    metadata = [doc.metadata for doc in documents]
    with open(f"{index_path}_metadata.json", "w") as f:
        json.dump(metadata, f)

    print(f"Created FAISS index at {index_path} with {len(documents)} documents")


def load_faiss_index(index_path: str):
    """
    Load a FAISS index and its metadata.

    Args:
        index_path: Path to the FAISS index

    Returns:
        Tuple of (index, metadata, documents)
    """
    try:
        # Load FAISS index
        index = faiss.read_index(f"{index_path}.faiss")

        # Load metadata
        with open(f"{index_path}_metadata.json", "r") as f:
            metadata = json.load(f)

        return index, metadata
    except FileNotFoundError:
        print(f"Index not found at {index_path}")
        return None, None


def search_faiss_index(
    query: str,
    index,
    metadata: List[Dict],
    top_k: int,
    embedding_model: str = "text-embedding-ada-002",
):
    """
    Search a FAISS index for similar documents.

    Args:
        query: Search query
        index: FAISS index
        metadata: Document metadata
        top_k: Number of results to return
        embedding_model: OpenAI embedding model to use

    Returns:
        List of (score, document_content) tuples
    """
    if index is None or metadata is None:
        return []

    # Get query embedding
    embeddings = OpenAIEmbeddings(model=embedding_model)
    query_embedding = embeddings.embed_query(query)
    query_vector = np.array([query_embedding]).astype("float32")

    # Search index
    scores, indices = index.search(query_vector, top_k)

    # Return results
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < len(metadata):
            results.append((float(score), metadata[idx]))

    return results


def format_retrieved_content(
    authored_results: List, descriptive_results: List, external_results: List
) -> str:
    """
    Format retrieved content for inclusion in the prompt.

    Args:
        authored_results: Results from authored text search
        descriptive_results: Results from descriptive sources search
        external_results: Results from external knowledge search

    Returns:
        Formatted string for prompt inclusion
    """
    formatted = ""

    if authored_results:
        formatted += "=== WITTGENSTEIN'S WRITINGS (for style reference) ===\n"
        for i, (score, metadata) in enumerate(authored_results, 1):
            formatted += f"{i}. {metadata.get('content', 'No content')}\n\n"

    if descriptive_results:
        formatted += "=== PHILOSOPHICAL CONTEXT ===\n"
        for i, (score, metadata) in enumerate(descriptive_results, 1):
            formatted += f"{i}. {metadata.get('content', 'No content')}\n\n"

    if external_results:
        formatted += "=== EXTERNAL KNOWLEDGE (for factual context) ===\n"
        for i, (score, metadata) in enumerate(external_results, 1):
            formatted += f"{i}. {metadata.get('content', 'No content')}\n\n"

    return formatted


def truncate_text(text: str, max_tokens: int = 1000) -> str:
    """
    Truncate text to approximately max_tokens.

    Args:
        text: Text to truncate
        max_tokens: Maximum number of tokens (roughly 4 characters per token)

    Returns:
        Truncated text
    """
    max_chars = max_tokens * 4  # Rough approximation
    if len(text) <= max_chars:
        return text

    # Try to truncate at a sentence boundary
    truncated = text[:max_chars]
    last_period = truncated.rfind(".")
    last_exclamation = truncated.rfind("!")
    last_question = truncated.rfind("?")

    last_sentence_end = max(last_period, last_exclamation, last_question)

    if (
        last_sentence_end > max_chars * 0.8
    ):  # If we found a sentence end in the last 20%
        return truncated[: last_sentence_end + 1]
    else:
        return truncated + "..."
