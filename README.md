# AI Data Assistant

A powerful AI assistant that provides intelligent insights about businesses using local LLM analysis and live Yelp data integration. Combines vector search on local CSV data with real-time business insights powered by RAG (Retrieval-Augmented Generation).

## Features

- **Dual Mode Processing**:
  - 💬 **Chat Tab**: Vector search on local business reviews (no API calls, completely free)
  - 🔍 **Search Tab**: Live Yelp API integration with AI-powered business insights
- **LLM Analysis**: Uses Ollama with Llama 3.2 model for intelligent responses
- **RAG Pipeline**: Retrieves relevant data and augments LLM prompts for accurate answers
- **Business Insights**: AI analysis of Yelp businesses (summary, sentiment, vibe, best for)
- **Smart Caching**: Prevents duplicate API calls, optimizes Yelp quota usage
- **Web Interface**: Beautiful, responsive Flask web app with light theme
- **Export Conversations**: Save chat history to PDF or Text formats
- **API Usage Tracking**: Monitor Yelp API calls and remaining quota in real-time

## Requirements

- Python 3.8+
- Ollama (with `llama3.2` and `mxbai-embed-large` models)
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ai-data-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure Ollama is running locally (default: http://localhost:11434)

## Usage

### Option 1: Web Interface (Recommended) 🌐

Run the Flask web app:
```bash
python app.py
```

Then open your browser:
```
http://localhost:5000
```

**Features:**
- Clean, intuitive chat interface
- Ask questions directly
- Export conversations to PDF/Text
- Clear history with one click

### Option 2: Command Line Interface 💻

Run the interactive chatbot:
```bash
python main.py
```

**Commands:**
- `q` - Quit
- `export txt` - Export to text file
- `export pdf` - Export to PDF file
- `clear` - Clear conversation history
- `help` - Show commands

## Project Structure

- `app.py` - Flask web interface
- `main.py` - Command-line chatbot
- `vector.py` - Vector store initialization and retrieval
- `export.py` - PDF and text export functionality
- `templates/` - HTML templates for web interface
- `realistic_restaurant_reviews.csv` - Business review dataset (sample: restaurant data)
- `requirements.txt` - Python dependencies
- `exports/` - Directory for exported conversations

## How It Works

### Overview

1. **Data Loading**: Business reviews from CSV are loaded and processed
2. **Embeddings**: Reviews are converted to embeddings using `mxbai-embed-large`
3. **Vector Store**: Embeddings are stored in Chroma database
4. **Retrieval**: When you ask a question, the 5 most relevant reviews are retrieved
5. **Generation**: The LLM generates an answer based on the retrieved reviews

### Detailed Workflow

1. **Load Business Reviews**
   - Reads `realistic_restaurant_reviews.csv` (or any business review CSV)
   - Contains reviews with ratings and comments

2. **Create Vector Embeddings**
   - Uses Ollama with `mxbai-embed-large` model
   - Converts text reviews into numerical vectors
   - Stores in Chroma vector database

3. **User Input**
   - Run `python main.py`
   - Chatbot prompts: "Ask your question (q to quit):"
   - Example: "What do customers value most in this business?"

4. **Retrieve Relevant Reviews**
   - Converts your question to embeddings
   - Searches Chroma for semantically similar reviews
   - Fetches top matching business reviews

5. **Generate AI Response**
   - Sends retrieved reviews + question to Ollama LLM (Llama 3.2)
   - LLM combines context with local knowledge
   - Returns intelligent answer based on actual reviews

6. **Display Answer**
   - Shows AI-generated response
   - Loop back to step 3 or exit with 'q'

## Quick Start

1. Ensure **Ollama** is running: `http://localhost:11434`
2. Ensure `.env` file has `YELP_API_KEY` (for Search Tab)
3. Run the web interface: `python app.py`
4. Open: `http://localhost:5000`

### Chat Tab (Local - No API Calls)
Ask questions about local CSV data:
- "What do customers appreciate most?"
- "Which businesses offer good value?"
- "What are common complaints or praise?"

### Search Tab (Live Yelp API)
Search any business and get AI insights:
1. Search: "Coffee shops in New York" (or any business type)
2. Click "AI Insights" on any result
3. View: Summary, sentiment, vibe, best for, key remarks

## License

MIT
