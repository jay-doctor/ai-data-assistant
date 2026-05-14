from flask import Flask, render_template, request, jsonify, send_file
from vector import retriever
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from export import ExportManager
from live_data import search_businesses, get_business_reviews
from ai_insights import analyze_business

app = Flask(__name__)
export_manager = ExportManager()

model = OllamaLLM(model="llama3.2")
template = """
You are a helpful assistant.

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    question = request.json.get('question', '').strip()
    
    if not question:
        return jsonify({'error': 'Please enter a question'}), 400
    
    try:
        reviews = retriever.invoke(question)
        answer = chain.invoke({"reviews": reviews, "question": question})
        
        # Save to history
        export_manager.add_conversation(question, reviews, answer)
        
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export/txt', methods=['GET'])
def export_txt():
    filepath = export_manager.export_to_text()
    if filepath:
        filename = filepath.split('\\')[-1]
        return send_file(filepath, as_attachment=True, download_name=filename, mimetype='text/plain')
    return jsonify({'error': '❌ No history to export'}), 400

@app.route('/export/pdf', methods=['GET'])
def export_pdf():
    filepath = export_manager.export_to_pdf()
    if filepath:
        filename = filepath.split('\\')[-1]
        return send_file(filepath, as_attachment=True, download_name=filename, mimetype='application/pdf')
    return jsonify({'error': '❌ No history to export'}), 400

@app.route('/clear', methods=['POST'])
def clear():
    export_manager.clear_history()
    return jsonify({'message': 'History cleared'})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    location = request.args.get('location', 'New York').strip()
    
    if not query:
        return jsonify({'error': 'Please enter a search query'}), 400
    
    try:
        results = search_businesses(query, location)
        
        if isinstance(results, dict) and 'error' in results:
            return jsonify(results), 400
        
        return jsonify({'results': results, 'count': len(results)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/insights', methods=['GET'])
def insights():
    business_id = request.args.get('id', '').strip()
    name = request.args.get('name', 'Business').strip()
    
    if not business_id:
        return jsonify({'error': 'Business ID required'}), 400
    
    try:
        # Get reviews from Yelp
        reviews = get_business_reviews(business_id)
        
        # Analyze with LLM
        analysis = analyze_business(name, reviews)
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api-status', methods=['GET'])
def api_status():
    """Check current API usage"""
    from live_data import searcher
    return jsonify({
        'api_calls_made': searcher.api_calls,
        'limit': 5000,
        'remaining': 5000 - searcher.api_calls,
        'note': 'Resets monthly. Check Yelp dashboard for exact limits.'
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("AI DATA ASSISTANT - WEB INTERFACE")
    print("="*50)
    print("\nOpen your browser: http://localhost:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)
