from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(complaint_text: str, api_key: str = None) -> list:
    """
    Takes a complaint text and returns its embedding vector.
    Runs locally — no API key needed.
    api_key param kept so teammates don't need to change their code.

    Args:
        complaint_text: the raw complaint string from the user

    Returns:
        A list of floats — the embedding vector
    """
    vector = model.encode(complaint_text)
    return vector.tolist()