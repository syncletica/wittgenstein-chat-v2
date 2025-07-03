# Wittgenstein Chatbot

A terminal-based chatbot that role-plays as Ludwig Wittgenstein using Retrieval-Augmented Generation (RAG). The chatbot combines Wittgenstein's writings, philosophical commentary, and modern knowledge to provide contextually relevant responses in his style.

## Table of Contents
- [Quick Start](#quick-start)
- [Example Conversation](#example-conversation)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Setup and Data Ingestion](#setup-and-data-ingestion)
- [Data Sources](#data-sources)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Quick Start
```bash
pip install -r requirements.txt
python setup.py  # builds FAISS indexes from included data
python main.py
```

## Example Conversation
```
User: How would you describe the "private language" argument?
Bot: In ordinary language, the idea of a purely private language is incoherent. To understand a word is to master its public use, not to consult an inner diary. Thus, any "private" language would lack the criteria for correctness we rely on in everyday speech.
```

## Features
- **Three-tier RAG System**: Separate FAISS indexes for different knowledge types:
  - `authored_text`: Wittgenstein's own writings
  - `descriptive_sources`: Philosophical commentary
  - `external_knowledge`: Modern facts and concepts
- **Dynamic Prompt Construction** for contextually relevant prompts
- **OpenAI Integration** with GPT-4 or GPT-3.5-turbo
- **Conversation Memory** to maintain context
- **Terminal Interface** for interactive use

## Project Structure
```
├── main.py                 # Main application entry point
├── config.py               # Configuration settings
├── prompt_builder.py       # Dynamic prompt construction
├── retrievers/             # Knowledge retrieval modules
│   ├── __init__.py
│   ├── authored.py         # Wittgenstein's writings retriever
│   ├── descriptive.py      # Commentary retriever
│   └── external.py         # External knowledge retriever
├── loaders/                # Data ingestion modules
│   ├── __init__.py
│   └── ingest.py           # Data processing and indexing
├── data/                   # Text data directories
│   ├── authored_texts/     # Wittgenstein's writings
│   ├── descriptive_sources/# Commentary and analysis
│   └── external_knowledge/ # Modern facts and concepts
├── indexes/                # FAISS vector indexes
│   ├── faiss_authored/
│   ├── faiss_descriptive/
│   └── faiss_external/
└── utils.py                # Utility functions
```

## Installation
1. **Clone the repository**
   ```bash
git clone https://github.com/syncletica/wittgenstein-chat-v2.git
cd wittgenstein-chat-v2
```
2. **Install dependencies**
   ```bash
pip install -r requirements.txt
```
3. **Set up environment variables**
   ```bash
export OPENAI_API_KEY='your-api-key-here'
# Optional: enable LangSmith tracing
export LANGSMITH_API_KEY='your-langsmith-key'
export LANGSMITH_PROJECT='wittgenstein-chatbot'
```
   You can also create a `.env` file with the same variables.

## Setup and Data Ingestion
This repository includes sample data so you can start chatting immediately.

### Quick Setup (Recommended)
Run `python setup.py` to build FAISS indexes:
```bash
python setup.py
```

### Manual Setup (Alternative)
```bash
python -c "from loaders.ingest import DataIngester; DataIngester().ingest_all()"
```

## Data Sources
**authored_texts/** – Wittgenstein's writings
- [Tractatus Logico-Philosophicus](https://www.wittgensteinproject.org/w/index.php/Tractatus_Logico-Philosophicus_(English))
- [Blue Book](https://www.wittgensteinproject.org/w/index.php/Blue_Book)
- [Brown Book](https://www.wittgensteinproject.org/w/index.php/Brown_Book)
- [Lecture on Ethics](https://www.wittgensteinproject.org/w/index.php/Lecture_on_Ethics)

**descriptive_sources/** – Stanford Encyclopedia of Philosophy
- [Ludwig Wittgenstein](https://plato.stanford.edu/entries/wittgenstein/)
- [Private Language](https://plato.stanford.edu/entries/private-language/)
- [Rule Following](https://plato.stanford.edu/entries/rule-following/)
- [Wittgenstein's Aesthetics](https://plato.stanford.edu/entries/wittgenstein-aesthetics/)
- [Wittgenstein's Atomism](https://plato.stanford.edu/entries/wittgenstein-atomism/)
- [Wittgenstein's Philosophy of Mathematics](https://plato.stanford.edu/entries/wittgenstein-mathematics/)

**external_knowledge/** – arXiv papers
- [Understanding LLMs: A Comprehensive Overview from Training to Inference](https://arxiv.org/abs/2307.06435)

### Adding Your Own Data (Optional)
1. Add texts to the relevant `data/` subdirectories
2. Re-run the ingestion process:
   ```bash
   python -c "from loaders.ingest import DataIngester; DataIngester().ingest_all()"
   ```

## Usage
### Starting the Chatbot
```bash
python main.py
```

### Available Commands
- `help` – Show help information
- `clear` – Clear conversation history
- `status` – Show retriever status
- `quit`, `exit`, `bye` – Exit the chatbot

## Configuration
Edit `config.py` to adjust settings:
- **OpenAI Settings** – model, temperature, max tokens
- **Retrieval Settings** – number of results from each knowledge base
- **Embedding Settings** – chunk size, overlap, embedding model
- **Chat Settings** – conversation history length
- **LangSmith Tracing** – controlled by `LANGSMITH_API_KEY` and `LANGSMITH_PROJECT`

## How It Works
1. **Query Processing** – your question is processed and searches all knowledge bases
2. **Content Retrieval** – relevant passages are retrieved
3. **Prompt Construction** – builds a prompt with instructions, retrieved text, and history
4. **Response Generation** – OpenAI produces a reply in Wittgenstein's style
5. **Context Integration** – the reply incorporates retrieved knowledge

## Customization
- Add new data sources under `data/` and rerun ingestion
- Edit `prompt_template.md` to adjust Wittgenstein's style
- Tune retrieval settings via `TOP_K_*` in `config.py`

## Requirements
- Python 3.8+
- OpenAI API key
- Internet connection for API calls

## Dependencies
- `langchain`
- `langchain-openai`
- `faiss-cpu`
- `openai`
- `python-dotenv`
- `tiktoken`
- `numpy`

## Troubleshooting
### Common Issues
1. **"No retrievers available"** – run the data ingestion process first
2. **"OpenAI API key required"** – ensure your API key is set
3. **Slow responses** – try GPT-3.5-turbo
4. **Memory issues** – reduce chunk size or retrieval counts

### Performance Tips
- Use GPT-3.5-turbo for faster responses
- Reduce `TOP_K_*` values for quicker retrieval
- Limit conversation history length
- Use smaller chunk sizes for large documents

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## License
This project is licensed under the [MIT License](LICENSE).
