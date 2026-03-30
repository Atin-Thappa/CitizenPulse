import sqlite3
DB_PATH = "citizenpulse.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_complaint(citizen_name, citizen_email, raw_text, category, district, cluster_id=None):
    
    if not raw_text or not district:
        return {
            "success": False,
            "error": "raw_text and district are required"
        }

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO complaints 
        (citizen_name, citizen_email, raw_text, category, district, cluster_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (citizen_name, citizen_email, raw_text, category, district, cluster_id))

        conn.commit()

        complaint_id = cursor.lastrowid

        return {
            "success": True,
            "complaint_id": complaint_id,
            "message": "Complaint stored successfully"
        }

    except sqlite3.Error as e:
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        conn.close()


def create_cluster(cluster_name="General Issue", initial_score=1.0):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO clusters (cluster_name, aggregated_urgency_score)
    VALUES (?, ?)
    """, (cluster_name, initial_score))

    conn.commit()
    cluster_id = cursor.lastrowid

    conn.close()
    return cluster_id

def update_cluster_score(cluster_id, increment=1.0):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE clusters
    SET aggregated_urgency_score = aggregated_urgency_score + ?
    WHERE cluster_id = ?
    """, (increment, cluster_id))

    conn.commit()
    conn.close()

def find_existing_cluster(category, district):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT cluster_id 
    FROM complaints
    WHERE category = ? AND district = ?
    LIMIT 1
    """, (category, district))

    result = cursor.fetchone()
    conn.close()

    return result["cluster_id"] if result else None

def process_complaint(citizen_name, citizen_email, raw_text, category, district):

    cluster_id = find_existing_cluster(category, district)

    if cluster_id:
        update_cluster_score(cluster_id)
    else:
        cluster_id = create_cluster(cluster_name=category)

    result = create_complaint(
        citizen_name,
        citizen_email,
        raw_text,
        category,
        district,
        cluster_id
    )

    return {
        "success": True,
        "cluster_id": cluster_id,
        "complaint_result": result
    }

def get_all_clusters():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM clusters
    ORDER BY aggregated_urgency_score DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_complaints_by_cluster(cluster_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM complaints
    WHERE cluster_id = ?
    ORDER BY complaint_id DESC
    """, (cluster_id,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_heatmap_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT district, COUNT(*) as complaint_count
    FROM complaints
    GROUP BY district
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def update_complaint_status(complaint_id, status):
    """
    status should be: 'Pending', 'In-Progress', 'Resolved'
    """

    valid_status = ["Pending", "In-Progress", "Resolved"]

    if status not in valid_status:
        return {
            "success": False,
            "error": "Invalid status"
        }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE complaints
    SET status = ?
    WHERE complaint_id = ?
    """, (status, complaint_id))

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return {
            "success": False,
            "error": "Complaint not found"
        }

    conn.close()

    return {
        "success": True,
        "message": "Status updated successfully"
    }


# from database import create_complaint

# result = create_complaint(
#     citizen_name="Rahul Sharma",
#     citizen_email="rahul@gmail.com",
#     raw_text="Garbage not collected for 3 days",
#     category="Sanitation",
#     district="Rohini",
#     cluster_id=None  # will come later from AI
# )

# print(result)
