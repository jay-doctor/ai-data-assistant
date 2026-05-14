# Local AI Agent

A local AI-powered chatbot that answers questions about restaurant reviews using LangChain, Ollama embeddings, and Chroma vector database.

## Features

- **Local LLM**: Uses Ollama with Llama 3.2 model
- **Vector Search**: Retrieves relevant restaurant reviews using embeddings
- **RAG (Retrieval-Augmented Generation)**: Combines retrieved reviews with LLM for accurate answers
- **No API Keys Required**: Runs entirely locally
- **Export Conversations**: Save chat history to PDF or Text formats
- **Conversation History**: Track all Q&A exchanges in a session

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

### Commands

Once the chatbot is running, you can use these commands:

| Command | Description |
|---------|-------------|
| `q` | Quit the application |
| `export txt` | Export conversation history to text file |
| `export pdf` | Export conversation history to PDF file |
| `history` | View conversation history summary |
| `clear` | Clear conversation history |
| `help` | Show available commands |

### Example

```
Ask your question (q to quit, help for commands): What are the best Italian restaurants?

[AI generates answer based on restaurant reviews]

💡 Tip: Use 'export txt' or 'export pdf' to save this conversation!
```

### Export Features

- **Export to Text**: Save conversations to `.txt` file
- **Export to PDF**: Save formatted conversations to `.pdf` file
- All exports are saved to `./exports` folder
- Exports include timestamps, questions, source reviews, and answers

## Project Structure

- `main.py` - Main chatbot interface with command handling
- `vector.py` - Vector store initialization and retriever setup
- `export.py` - Export functionality (PDF and text export)
- `realistic_restaurant_reviews.csv` - Restaurant review dataset
- `requirements.txt` - Python dependencies
- `exports/` - Directory for exported conversations

## How It Works

### Overview

1. **Data Loading**: Restaurant reviews from CSV are loaded and processed
2. **Embeddings**: Reviews are converted to embeddings using `mxbai-embed-large`
3. **Vector Store**: Embeddings are stored in Chroma database
4. **Retrieval**: When you ask a question, the 5 most relevant reviews are retrieved
5. **Generation**: The LLM generates an answer based on the retrieved reviews

### Detailed Workflow

1. **Load Restaurant Reviews**
   - Reads `realistic_restaurant_reviews.csv`
   - Contains reviews with ratings and comments

2. **Create Vector Embeddings**
   - Uses Ollama with `mxbai-embed-large` model
   - Converts text reviews into numerical vectors
   - Stores in Chroma vector database

3. **User Input**
   - Run `python main.py`
   - Chatbot prompts: "Ask your question (q to quit):"
   - Example: "What are the best Italian restaurants?"

4. **Retrieve Relevant Reviews**
   - Converts your question to embeddings
   - Searches Chroma for semantically similar reviews
   - Fetches top matching restaurant reviews

5. **Generate AI Response**
   - Sends retrieved reviews + question to Ollama LLM (Llama 3.2)
   - LLM combines context with local knowledge
   - Returns intelligent answer based on actual reviews

6. **Display Answer**
   - Shows AI-generated response
   - Loop back to step 3 or exit with 'q'

## Questions to Try

**About Quality:**

"What are the best pizza restaurants?"
"Which places have the best crust?"
"What restaurants offer good value for money?"

**About Specific Styles:**

"What are the best New York style pizzas?"
"Do you have recommendations for Detroit-style pizza?"
"Which restaurants serve Neapolitan pizza?"

**About Ingredients:**

"What pizzas have the best fresh ingredients?"
"Which places use high-quality cheese?"
"What are the best toppings you've seen?"

**About Dietary Needs:**

"Are there good gluten-free options?"
"Which restaurants have vegan pizza?"
"What are the best options for people with allergies?"

**About Experience:**

"Which restaurants have good customer service?"
"Where can I take my kids?"
"Which places are good for large groups?"

**About Specific Aspects:**

"What makes a good pizza sauce?"
"Which restaurants are best for late-night eating?"
"What's the most popular pepperoni pizza?"

## License

MIT
