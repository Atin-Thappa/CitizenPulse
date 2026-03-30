import sqlite3
import json
import bcrypt
import numpy as np
from sentence_transformers import SentenceTransformer

DB_PATH = "mydata.db"

# Load model once
model = SentenceTransformer('all-MiniLM-L6-v2')

# ---------------- AUTH ----------------
def add_officer(email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO officers (email, password) VALUES (?, ?)",
                (email, hashed)
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def verify_officer(email, password):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM officers WHERE email=?", (email,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode(), result[0]):
            return True
        return False


# ---------------- EMBEDDING ----------------
def get_embedding(text):
    return model.encode(text).tolist()


def cosine_similarity(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


# ---------------- DB CONNECTION ----------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- EMBEDDING STORAGE ----------------
def store_embedding(complaint_id, vector):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO embeddings (complaint_id, vector)
    VALUES (?, ?)
    """, (complaint_id, json.dumps(vector)))

    conn.commit()
    conn.close()


def get_all_embeddings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM embeddings")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------------- CLUSTER LOGIC ----------------
def find_similar_cluster(new_embedding, threshold=0.75):
    embeddings = get_all_embeddings()

    best_match = None
    best_score = 0

    for row in embeddings:
        stored_vector = json.loads(row["vector"])
        score = cosine_similarity(new_embedding, stored_vector)

        if score > best_score and score > threshold:
            best_score = score
            best_match = row["complaint_id"]

    if best_match:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT cluster_id FROM complaints WHERE complaint_id=?",
            (best_match,)
        )
        result = cursor.fetchone()
        conn.close()

        return result["cluster_id"] if result else None

    return None


def create_cluster(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO clusters (cluster_name, aggregated_urgency_score)
    VALUES (?, 0)
    """, (name,))

    conn.commit()
    cid = cursor.lastrowid
    conn.close()
    return cid


def update_cluster_score(cluster_id, urgency):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE clusters
    SET aggregated_urgency_score = aggregated_urgency_score + ?
    WHERE cluster_id=?
    """, (urgency, cluster_id))

    conn.commit()
    conn.close()


# ---------------- COMPLAINT ----------------
def create_complaint(name, email, text, category, district, cluster_id, urgency):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO complaints
    (citizen_name, citizen_email, raw_text, category, district, cluster_id, urgency_score)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, email, text, category, district, cluster_id, urgency))

    conn.commit()
    cid = cursor.lastrowid
    conn.close()
    return cid
def get_urgency(text):
    text = text.lower()

    if "fire" in text or "accident" in text:
        return 10
    elif "water" in text:
        return 8
    elif "electricity" in text:
        return 7
    elif "garbage" in text:
        return 6
    else:
        return 5

# ---------------- MAIN PIPELINE ----------------
def process_complaint(name, email, text, category, district):

    # 1. embedding
    embedding = get_embedding(text)

    # 2. cluster
    cluster_id = find_similar_cluster(embedding)
    if not cluster_id:
        cluster_id = create_cluster(category)

    # 3. urgency (dummy for now)
    urgency = get_urgency(text)

    # 4. store complaint
    complaint_id = create_complaint(
        name, email, text, category, district, cluster_id, urgency
    )

    # 5. store embedding
    store_embedding(complaint_id, embedding)

    # 6. update cluster
    update_cluster_score(cluster_id, urgency)

    return {
        "complaint_id": complaint_id,
        "cluster_id": cluster_id,
        "urgency": urgency
    }


# ---------------- DASHBOARD ----------------
def get_clusters():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clusters ORDER BY aggregated_urgency_score DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_heatmap():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT district, COUNT(*) as count
    FROM complaints GROUP BY district
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]