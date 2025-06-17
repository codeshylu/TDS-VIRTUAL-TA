from flask import Flask, request, jsonify
from flask_cors import CORS
from search_utils import load_knowledge, create_embeddings, search
import os

app = Flask(__name__)
CORS(app)

# Load data and generate embeddings only once
try:
    data = load_knowledge()
    if not data:
        raise ValueError("No knowledge data found to embed.")
    
    texts, embeddings = create_embeddings(data)
    if not texts or embeddings is None or len(embeddings) == 0:
        raise ValueError("Embedding generation failed. Embeddings are empty.")

except Exception as e:
    print(f"🚨 Initialization Error: {e}")
    texts, embeddings = [], []

@app.route('/')
def home():
    return '✅ Virtual TA API is running. Use POST request at /api/'

@app.route('/api/', methods=['POST'])
def answer_query():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"answer": "Please provide a valid question."})

        if not texts or not embeddings:
            return jsonify({"answer": "Service is temporarily unavailable due to an embedding error."})

        best_match = search(question, texts, embeddings)
        return jsonify({"answer": best_match})
    
    except Exception as e:
        return jsonify({"answer": f"Error occurred: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)




