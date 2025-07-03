# Wittgenstein Chatbot

A terminal-based chatbot that role-plays as Ludwig Wittgenstein using Retrieval-Augmented Generation (RAG). The chatbot combines Wittgenstein's own writings, philosophical commentary, and external knowledge to provide contextually relevant responses in his distinctive style.

## Quick Start

```bash
pip install -r requirements.txt
python setup.py  # builds FAISS indexes from included data
python main.py
```

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
   git clone https://github.com/syncletica/wittgenstein-chat-v2.git
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

This repository comes pre-loaded with a comprehensive collection of Wittgenstein's writings, philosophical commentary, and modern knowledge sources. You can start using the chatbot immediately by running the setup script.

### Quick Setup (Recommended)

Run `python setup.py` to automatically build all FAISS indexes from the included data:

```bash
python setup.py
```

### Manual Setup (Alternative)

If you prefer to run the indexing process manually:

```bash
python -c "from loaders.ingest import DataIngester; DataIngester().ingest_all()"
```



## Data Sources

**authored_texts/** - Wittgenstein's Writings:
- [Tractatus Logico-Philosophicus](https://www.wittgensteinproject.org/w/index.php/Tractatus_Logico-Philosophicus_(English))
- [Blue Book](https://www.wittgensteinproject.org/w/index.php/Blue_Book)
- [Brown Book](https://www.wittgensteinproject.org/w/index.php/Brown_Book)
- [Lecture on Ethics](https://www.wittgensteinproject.org/w/index.php/Lecture_on_Ethics)

**descriptive_sources/** - Stanford Encyclopedia of Philosophy:
- [Ludwig Wittgenstein](https://plato.stanford.edu/entries/wittgenstein/)
- [Private Language](https://plato.stanford.edu/entries/private-language/)
- [Rule Following](https://plato.stanford.edu/entries/rule-following/)
- [Wittgenstein's Aesthetics](https://plato.stanford.edu/entries/wittgenstein-aesthetics/)
- [Wittgenstein's Atomism](https://plato.stanford.edu/entries/wittgenstein-atomism/)
- [Wittgenstein's Philosophy of Mathematics](https://plato.stanford.edu/entries/wittgenstein-mathematics/)

**external_knowledge/** - arXiv Papers:
- [Understanding LLMs: A Comprehensive Overview from Training to Inference](https://arxiv.org/abs/2307.06435)
- [Philosophical Introduction to Large Language Models](https://arxiv.org/abs/2307.06435)
- [Comprehensive Overview of Large Language Models](https://arxiv.org/abs/2307.06435)

### Adding Your Own Data (Optional)

You can enhance the chatbot by adding additional sources:

1. **Add Wittgenstein's writings** to `data/authored_texts/`
2. **Add philosophical commentary** to `data/descriptive_sources/`
3. **Add modern knowledge** to `data/external_knowledge/`
4. **Re-run the ingestion process**:
   ```bash
   python -c "from loaders.ingest import DataIngester; DataIngester().ingest_all()"
   ```

**Note**: The FAISS indexes are automatically regenerated when you run the ingestion process, so your new data will be included in future conversations.

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

## Configuration

Edit `config.py` to customize:

- **OpenAI Settings**: Model choice, temperature, max tokens
- **Retrieval Settings**: Number of results from each knowledge base
- **Embedding Settings**: Chunk size, overlap, embedding model
- **Chat Settings**: Conversation history length

### LangSmith Tracing (optional)

Set `LANGSMITH_API_KEY` and `LANGSMITH_PROJECT` to enable LangSmith tracing.
This provides observability through the LangSmith dashboard and is not required
for normal operation.

```bash
export LANGSMITH_API_KEY='your-langsmith-key'
export LANGSMITH_PROJECT='wittgenstein-chatbot'
```

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

Edit the system prompt in `prompt_template.md` to adjust:
- Philosophical approach
- Writing style
- Response characteristics

Response length is guided by the **Response Length** section of `prompt_template.md` and by `Config.MAX_TOKENS` in `config.py`.

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
