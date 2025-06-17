from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load your forum and course data from prepared files
def load_knowledge():
    data = []

    forum_path = 'forum_text.json'
    course_path = 'course_text.json'

    if os.path.exists(forum_path):
        with open(forum_path, 'r', encoding='utf-8') as f:
            forum_data = json.load(f)
            data.extend(forum_data)

    if os.path.exists(course_path):
        with open(course_path, 'r', encoding='utf-8') as f:
            course_data = json.load(f)
            data.extend(course_data)

    return data

# Create embeddings
def create_embeddings(data):
    texts = [item['text'] for item in data if 'text' in item and item['text'].strip()]
    if not texts:
        return [], None
    embeddings = model.encode(texts, convert_to_tensor=True)
    return texts, embeddings

# Search function
def search(query, texts, embeddings):
    if not texts or embeddings is None:
        return "Knowledge base is empty. Please check your data files."
    
    query_embedding = model.encode([query], convert_to_tensor=True)
    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_index = scores.argmax()
    return texts[top_index]

