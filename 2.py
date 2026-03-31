<<<<<<< HEAD
import requests

BASE_URL = "http://127.0.0.1:8000"
session = requests.Session() # This handles cookies automatically

def test_workflow():
    # 1. Register an Officer
    print("1. Registering Officer...")
    reg_data = {"email": "admin@city.gov", "password": "securepassword123"}
    requests.post(f"{BASE_URL}/register-officer", json=reg_data)

    # 2. Login as Officer
    print("2. Logging in...")
    login_data = {"email": "admin@city.gov", "password": "securepassword123"}
    response = session.post(f"{BASE_URL}/login", json=login_data)
    print(f"Login Status: {response.status_code}")

    # 3. Submit a Complaint (as a Citizen)
    # 3. Submit a Complaint
    print("3. Submitting Complaint...")
    # INCORRECT (Using commas instead of colons makes it a SET)
    # CORRECT (Notice the COLONS :)
    complaint_data = {
    "citizen_name": "Rahul Kumar",
    "citizen_email": "rahul@example.com",
    "raw_text": "Huge fire near the market!",
    "category": "Emergency",
    "district": "North Delhi"
}
    comp_resp = requests.post(f"{BASE_URL}/complaint", json=complaint_data)

# ADD THIS LINE TO SEE THE ERROR:
    if comp_resp.status_code != 200:
       print(f"SERVER ERROR: {comp_resp.text}") 
       return

    comp_id = comp_resp.json().get("complaint_id")

    # 4. View Dashboard (Officer Only)
    print("4. Checking Dashboard Clusters...")
    clusters = session.get(f"{BASE_URL}/clusters")
    print(f"Found {len(clusters.json())} clusters.")

    # 5. Resolve Complaint
    print(f"5. Resolving Complaint #{comp_id}...")
    # Note: Status is passed as a query parameter in your FastAPI put route
    res = session.put(f"{BASE_URL}/complaint/{comp_id}/status?status=Resolved")
    print(f"Final Result: {res.json()}")

if __name__ == "__main__":
=======
import requests

BASE_URL = "http://127.0.0.1:8000"
session = requests.Session() # This handles cookies automatically

def test_workflow():
    # 1. Register an Officer
    print("1. Registering Officer...")
    reg_data = {"email": "admin@city.gov", "password": "securepassword123"}
    requests.post(f"{BASE_URL}/register-officer", json=reg_data)

    # 2. Login as Officer
    print("2. Logging in...")
    login_data = {"email": "admin@city.gov", "password": "securepassword123"}
    response = session.post(f"{BASE_URL}/login", json=login_data)
    print(f"Login Status: {response.status_code}")

    # 3. Submit a Complaint (as a Citizen)
    # 3. Submit a Complaint
    print("3. Submitting Complaint...")
    # INCORRECT (Using commas instead of colons makes it a SET)
    # CORRECT (Notice the COLONS :)
    complaint_data = {
    "citizen_name": "Rahul Kumar",
    "citizen_email": "rahul@example.com",
    "raw_text": "Huge fire near the market!",
    "category": "Emergency",
    "district": "North Delhi"
}
    comp_resp = requests.post(f"{BASE_URL}/complaint", json=complaint_data)

# ADD THIS LINE TO SEE THE ERROR:
    if comp_resp.status_code != 200:
       print(f"SERVER ERROR: {comp_resp.text}") 
       return

    comp_id = comp_resp.json().get("complaint_id")

    # 4. View Dashboard (Officer Only)
    print("4. Checking Dashboard Clusters...")
    clusters = session.get(f"{BASE_URL}/clusters")
    print(f"Found {len(clusters.json())} clusters.")

    # 5. Resolve Complaint
    print(f"5. Resolving Complaint #{comp_id}...")
    # Note: Status is passed as a query parameter in your FastAPI put route
    res = session.put(f"{BASE_URL}/complaint/{comp_id}/status?status=Resolved")
    print(f"Final Result: {res.json()}")

if __name__ == "__main__":
>>>>>>> 018686aab8fbf5bb520e42656d7230c1d94851f3
    test_workflow()