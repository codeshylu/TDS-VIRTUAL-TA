from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '✅ Virtual TA API is running. Use POST request at /api/'

@app.route('/api/', methods=['POST'])
def answer_query():
    data = request.get_json()
    question = data.get("question", "")
    
    # Placeholder logic - you will replace this with semantic search later
    if "deadline" in question.lower():
        return jsonify({"answer": "Please check the course calendar for deadlines."})
    else:
        return jsonify({"answer": "This is a placeholder response."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
