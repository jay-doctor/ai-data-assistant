# Local AI Agent

A local AI-powered chatbot that answers questions about restaurant reviews using LangChain, Ollama embeddings, and Chroma vector database.

## Features

- **Local LLM**: Uses Ollama with Llama 3.2 model
- **Vector Search**: Retrieves relevant restaurant reviews using embeddings
- **RAG (Retrieval-Augmented Generation)**: Combines retrieved reviews with LLM for accurate answers
- **No API Keys Required**: Runs entirely locally

## Requirements

- Python 3.8+
- Ollama (with `llama3.2` and `mxbai-embed-large` models)
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jay-doctor/local-ai-agent.git
cd local-ai-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure Ollama is running locally (default: http://localhost:11434)

## Usage

Run the interactive chatbot:
```bash
python main.py
```

Then ask questions about the restaurant reviews:
```
Ask your question (q to quit): What are the best Italian restaurants?
```

## Project Structure

- `main.py` - Main chatbot interface
- `vector.py` - Vector store initialization and retriever setup
- `realistic_restaurant_reviews.csv` - Restaurant review dataset
- `requirements.txt` - Python dependencies

## How It Works

1. **Data Loading**: Restaurant reviews from CSV are loaded and processed
2. **Embeddings**: Reviews are converted to embeddings using `mxbai-embed-large`
3. **Vector Store**: Embeddings are stored in Chroma database
4. **Retrieval**: When you ask a question, the 5 most relevant reviews are retrieved
5. **Generation**: The LLM generates an answer based on the retrieved reviews

## License

MIT
