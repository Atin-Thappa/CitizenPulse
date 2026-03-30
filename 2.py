import requests

# The URL where your FastAPI is running (default uvicorn port)
URL = "http://127.0.0.1:8000/login"

# Change these to match a user already in your 'officers' table
data = {
    "email": "officer@gov.in",
    "password": "password"
}

try:
    # 1. Send the POST request
    response = requests.post(URL, json=data)

    # 2. Check the results
    print(f"--- Status Code: {response.status_code} ---")
    
    if response.status_code == 200:
        print("✅ Login Successful!")
        print(f"Server Response: {response.json()}")
        print(f"Cookies Received: {response.cookies.get_dict()}")
    else:
        print("❌ Login Failed.")
        print(f"Error Detail: {response.json()}")

except requests.exceptions.ConnectionError:
    print("❌ Error: Is your FastAPI server running? (Run 'uvicorn main:app --reload' first)")
URL = "http://127.0.0.1:8000/complaint"

data = {
    "citizen_name": "Rahul",
    "citizen_email": "rahul@gmail.com",
    "raw_text": "Garbage not collected for 3 days",
    "category": "Sanitation",
    "district": "Rohini"
}