import sqlite3

DB_PATH = "mydata.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ---------------- OFFICERS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS officers (
        officer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # ---------------- CLUSTERS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clusters (
        cluster_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cluster_name TEXT,
        aggregated_urgency_score REAL DEFAULT 0
    )
    """)

    # ---------------- COMPLAINTS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
        citizen_name TEXT,
        citizen_email TEXT,
        raw_text TEXT,
        category TEXT,
        district TEXT,
        cluster_id INTEGER,
        urgency_score REAL,
        status TEXT,
        created_at TEXT,
        FOREIGN KEY (cluster_id) REFERENCES clusters(cluster_id)
    )
    """)

    # ---------------- EMBEDDINGS ----------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        complaint_id INTEGER,
        vector TEXT,
        FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id)
    )
    """)

    conn.commit()
    conn.close()

    print("✅ Database & tables created successfully!")

if __name__ == "__main__":
    create_tables()