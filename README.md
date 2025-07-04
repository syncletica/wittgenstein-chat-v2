# Wittgenstein Chatbot

A personal terminal chatbot that role-plays as Ludwig Wittgenstein using RAG. Combines his writings, philosophical commentary, and modern knowledge to respond in his style.

## Quick Start

```bash
pip install -r requirements.txt
export OPENAI_API_KEY='your-api-key-here'
python setup.py
python main.py
```

## What it does

- **Three knowledge bases**: Wittgenstein's writings, philosophical commentary, modern facts
- **RAG-powered**: Retrieves relevant content for each response
- **Authentic style**: Responds as Wittgenstein would, with numbered propositions and probing questions
- **Terminal interface**: Simple chat interface with conversation memory

## Data sources

- **Writings**: Tractatus, Philosophical Investigations
- **Commentary**: Stanford Encyclopedia articles on Wittgenstein, private language, rule-following, aesthetics
- **Modern knowledge**: LLM papers for contemporary context

## Commands

- `help` - Show commands
- `clear` - Clear history  
- `status` - Show retriever status
- `quit` - Exit

## Config

Edit `config.py` for:
- OpenAI model/temperature
- Retrieval counts
- Token limits
- Conversation history length

## Setup

The `setup.py` script builds FAISS indexes from the included data. No sample data creation - uses real sources.

## Dependencies

- langchain, langchain-openai
- faiss-cpu, openai
- python-dotenv, tiktoken
