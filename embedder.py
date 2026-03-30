from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(complaint_text: str) -> list:
    vector = model.encode(complaint_text)
    return vector.tolist()