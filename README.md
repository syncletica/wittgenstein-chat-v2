# Wittgenstein Chatbot

A terminal-based chatbot that role-plays as Ludwig Wittgenstein using Retrieval-Augmented Generation (RAG). The chatbot combines Wittgenstein's own writings, philosophical commentary, and external knowledge to provide contextually relevant responses in his distinctive style.

## Features

- **Three-tier RAG System**: Uses separate FAISS indexes for different types of knowledge:
  - `authored_text`: Wittgenstein's own writings (for style and approach)
  - `descriptive_sources`: Commentary about his thought (for philosophical context)
  - `external_knowledge`: Facts outside his time (for modern context)
- **Dynamic Prompt Construction**: Builds contextually relevant prompts using retrieved content
- **OpenAI Integration**: Uses GPT-4 or GPT-3.5-turbo for generating responses
- **Conversation Memory**: Maintains conversation history for contextual responses
- **Terminal Interface**: Clean, interactive command-line interface

## Project Structure

```
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── prompt_builder.py      # Dynamic prompt construction
├── retrievers/           # Knowledge retrieval modules
│   ├── __init__.py
│   ├── authored.py       # Wittgenstein's writings retriever
│   ├── descriptive.py    # Commentary retriever
│   └── external.py       # External knowledge retriever
├── loaders/              # Data ingestion modules
│   ├── __init__.py
│   └── ingest.py         # Data processing and indexing
├── data/                 # Text data directories
│   ├── authored_texts/   # Wittgenstein's writings
│   ├── descriptive_sources/ # Commentary and analysis
│   └── external_knowledge/  # Modern facts and concepts
├── indexes/              # FAISS vector indexes
│   ├── faiss_authored/
│   ├── faiss_descriptive/
│   └── faiss_external/
└── utils.py              # Utility functions
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd wittgenstein-chat-v2
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key**:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Setup and Data Ingestion

1. **Create sample data** (for testing):
   ```bash
   python -c "from loaders.ingest import DataIngester; DataIngester().create_sample_data()"
   ```

2. **Ingest and index the data**:
   ```bash
   python -c "from loaders.ingest import DataIngester; DataIngester().ingest_all()"
   ```

3. **Add your own data** (optional):
   - Place Wittgenstein's writings in `data/authored_texts/`
   - Add philosophical commentary in `data/descriptive_sources/`
   - Include modern knowledge in `data/external_knowledge/`
   - Re-run the ingestion process

## Usage

### Starting the Chatbot

```bash
python main.py
```

### Available Commands

- `help` - Show help information
- `clear` - Clear conversation history
- `status` - Show retriever status
- `quit`, `exit`, `bye` - Exit the chatbot

### Example Conversation

```
============================================================
WITTGENSTEIN CHATBOT
============================================================
You are now conversing with Ludwig Wittgenstein.
Type 'quit', 'exit', or 'bye' to end the conversation.
Type 'help' for available commands.
============================================================

You: What is the meaning of life?

Wittgenstein: The question "What is the meaning of life?" is itself a confusion. 
It assumes that "meaning" is something that can be found, like a hidden object. 
But meaning is not a thing - it is how we use words in our language games. 
The question arises from a misunderstanding of how language works.

You: How should I think about artificial intelligence?

Wittgenstein: When you speak of "artificial intelligence," what language game 
are you playing? Are you asking about machines that calculate, or about 
consciousness, or about something else entirely? The confusion begins when 
we treat "intelligence" as if it were a single, well-defined thing. 
Look at how we actually use the word "intelligent" in different contexts - 
that will show you what the concept amounts to.
```

## Configuration

Edit `config.py` to customize:

- **OpenAI Settings**: Model choice, temperature, max tokens
- **Retrieval Settings**: Number of results from each knowledge base
- **Embedding Settings**: Chunk size, overlap, embedding model
- **Chat Settings**: Conversation history length

## How It Works

1. **Query Processing**: When you ask a question, the system searches all three knowledge bases
2. **Content Retrieval**: Relevant passages are retrieved from:
   - Wittgenstein's writings (for style and approach)
   - Philosophical commentary (for context)
   - External knowledge (for modern facts)
3. **Prompt Construction**: A dynamic prompt is built combining:
   - System instructions for Wittgenstein's role
   - Retrieved content from all sources
   - Conversation history
   - Your current question
4. **Response Generation**: OpenAI generates a response in Wittgenstein's style
5. **Context Integration**: The response incorporates retrieved knowledge without direct quotation

## Customization

### Adding New Data Sources

1. Add text files to the appropriate `data/` subdirectory
2. Re-run the ingestion process
3. The system will automatically include the new content

### Modifying Wittgenstein's Style

Edit the system prompt in `prompt_builder.py` to adjust:
- Philosophical approach
- Writing style
- Response characteristics

### Adjusting Retrieval

Modify the `TOP_K_*` settings in `config.py` to control how much content is retrieved from each knowledge base.

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for API calls

## Dependencies

- `langchain` - RAG framework
- `langchain-openai` - OpenAI integration
- `faiss-cpu` - Vector similarity search
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `tiktoken` - Token counting
- `numpy` - Numerical operations

## Troubleshooting

### Common Issues

1. **"No retrievers available"**: Run the data ingestion process first
2. **"OpenAI API key required"**: Set your API key as an environment variable
3. **Slow responses**: Consider using GPT-3.5-turbo instead of GPT-4
4. **Memory issues**: Reduce chunk size or number of retrieved results

### Performance Tips

- Use GPT-3.5-turbo for faster responses
- Reduce `TOP_K_*` values for quicker retrieval
- Limit conversation history length
- Use smaller chunk sizes for large documents

## License

This project is for educational and research purposes. Please respect copyright when adding content to the knowledge bases.

## Contributing

Contributions are welcome! Areas for improvement:
- Additional knowledge base content
- Enhanced prompt engineering
- Better error handling
- Performance optimizations
- UI improvements 
