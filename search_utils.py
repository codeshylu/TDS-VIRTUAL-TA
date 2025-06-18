from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

# Load lightweight model (Render-friendly)
model = SentenceTransformer('paraphrase-albert-small-v2')

# Limit to avoid Render OOM issues
MAX_KNOWLEDGE_ITEMS = 500

# Load course and forum data from JSON files
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

    # Filter out empty or invalid text entries and apply item limit
    filtered_data = [item for item in data if 'text' in item and item['text'].strip()]
    limited_data = filtered_data[:MAX_KNOWLEDGE_ITEMS]
    print(f"✅ Loaded {len(limited_data)} items for embeddings")

    return limited_data

# Create embeddings
def create_embeddings(data):
    texts = [item['text'] for item in data]
    if not texts:
        return [], None
    embeddings = model.encode(texts, convert_to_tensor=True)
    return texts, embeddings

# Semantic search function
def search(query, texts, embeddings):
    if not texts or embeddings is None:
        return "Knowledge base is empty. Please check your data files."

    query_embedding = model.encode([query], convert_to_tensor=True)
    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_index = scores.argmax()
    return texts[top_index]



