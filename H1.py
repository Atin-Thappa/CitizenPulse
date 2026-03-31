import sqlite3
import json
import bcrypt
import numpy as np
from sentence_transformers import SentenceTransformer
from datetime import datetime

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
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO complaints
    (citizen_name, citizen_email, raw_text, category, district, cluster_id, urgency_score,created_at,status)
    VALUES (?, ?, ?, ?, ?, ?, ? , ? , ?)
    """, (name, email, text, category, district, cluster_id, urgency,created_at,'pending'))

    conn.commit()
    cid = cursor.lastrowid
    conn.close()
    return cid
def get_urgency(text):
    embedding = get_embedding(text)

    # Reference critical patterns
    critical_cases = [
        ("fire accident explosion", 10),
        ("water shortage no water supply", 8),
        ("electricity failure power outage", 7),
        ("garbage waste dumping", 6),
    ]

    max_score = 5  # default

    for case_text, score in critical_cases:
        case_embedding = get_embedding(case_text)
        similarity = cosine_similarity(embedding, case_embedding)

        if similarity > 0.6:
            max_score = max(max_score, score)

    return max_score
def can_submit_complaint(email, limit=2):
    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().date()

    cursor.execute("""
    SELECT COUNT(*) FROM complaints
    WHERE citizen_email=? AND DATE(created_at)=?
    """, (email, today))

    count = cursor.fetchone()[0]
    conn.close()

    return count < limit

# ---------------- MAIN PIPELINE ----------------
def process_complaint(name, email, text, category, district):
    if not can_submit_complaint(email):
         return {
           "error": "Daily complaint limit reached (max 2 per day)"
        }

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


import smtplib
from email.mime.text import MIMEText

def send_resolution_email(to_email, complaint_id):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"  # use app password

    subject = "Complaint Resolved"
    body = f"Your complaint (ID: {complaint_id}) has been resolved. Thank you!"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("Email error:", e)
        return False
def update_complaint_status(complaint_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    valid_status = ["Pending", "In-Progress", "Resolved"]

    if status not in valid_status:
        return {"success": False, "error": "Invalid status"}

    # Update status
    cursor.execute("""
    UPDATE complaints
    SET status=?
    WHERE complaint_id=?
    """, (status, complaint_id))

    if cursor.rowcount == 0:
        conn.close()
        return {"success": False, "error": "Complaint not found"}

    # If resolved → send email
    if status == "Resolved":
        cursor.execute("""
        SELECT citizen_email FROM complaints WHERE complaint_id=?
        """, (complaint_id,))
        result = cursor.fetchone()

        if result:
            send_resolution_email(result[0], complaint_id)

    conn.commit()
    conn.close()

    return {"success": True, "message": "Status updated"}
def get_complaints_by_cluster(cluster_id):
    conn = get_connection()
    cursor = conn.cursor()

    # We fetch all details so the officer knows WHO to contact and WHERE to go
    cursor.execute("""
    SELECT citizen_name, citizen_email, raw_text, district, urgency_score, status, created_at 
    FROM complaints
    WHERE cluster_id = ?
    ORDER BY created_at DESC
    """, (cluster_id,))

    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]