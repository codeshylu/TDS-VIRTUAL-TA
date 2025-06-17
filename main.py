from flask import Flask, request, jsonify
from flask_cors import CORS
from search_utils import load_knowledge, create_embeddings, search

app = Flask(__name__)
CORS(app)

# Load data and generate embeddings only once
data = load_knowledge()
texts, embeddings = create_embeddings(data)

@app.route('/')
def home():
    return '✅ Virtual TA API is running. Use POST request at /api/'

@app.route('/api/', methods=['POST'])
def answer_query():
    data = request.get_json()
    question = data.get("question", "")
    
    if not question:
        return jsonify({"answer": "Please provide a valid question."})
    
    best_match = search(question, texts, embeddings)
    return jsonify({"answer": best_match})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

