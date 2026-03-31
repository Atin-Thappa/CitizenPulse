<<<<<<< HEAD
from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import jwt
from datetime import datetime, timedelta
from fastapi import Cookie, Depends

# Import your custom files
import schema
import H1

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon (allow all)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SECRET_KEY = "your_hackathon_secret_key"

def get_current_user(officer_session: str = Cookie(None)):
    if not officer_session:
        raise HTTPException(status_code=401, detail="Not logged in")

    try:
        payload = jwt.decode(officer_session, SECRET_KEY, algorithms=["HS256"])
        return payload["email"]
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

@app.post("/register-officer")
async def register(data: schema.RegisterRequest):
    success = H1.add_officer(data.email, data.password)
    if not success:
        raise HTTPException(status_code=400, detail="Email already exists")
    return {"message": "Officer registered successfully"}

@app.post("/login")
async def login(data: schema.LoginRequest, response: Response):
    user = H1.verify_officer(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"email": data.email, "exp": datetime.utcnow() + timedelta(hours=24)}, 
        SECRET_KEY, 
        algorithm="HS256"
    )

    response.set_cookie(key="officer_session", value=token, httponly=True ,samesite="lax")
    return {"status": "success", "user": data.email}
# -------- COMPLAINT --------
@app.post("/complaint")
async def complaint(data: schema.ComplaintRequest):
    result = H1.process_complaint(
        data.citizen_name,
        data.citizen_email,
        data.raw_text,
        data.category,
        data.district
    )
    return result


# -------- DASHBOARD --------
@app.get("/clusters")
def clusters(user=Depends(get_current_user)):
    return H1.get_clusters()


@app.get("/heatmap")
def heatmap(user=Depends(get_current_user)):
    return H1.get_heatmap()


@app.put("/complaint/{complaint_id}/status")
def update_status(complaint_id: int, status: str):
    return H1.update_complaint_status(complaint_id, status)
@app.get("/clusters/{cluster_id}/complaints")
async def cluster_details(cluster_id: int, user=Depends(get_current_user)):
    """
    Only logged-in officers can see the specific 
    complaints inside a cluster.
    """
    details = H1.get_complaints_by_cluster(cluster_id)
    
    if not details:
        raise HTTPException(status_code=404, detail="No complaints found for this cluster")
        
    return {
        "cluster_id": cluster_id,
        "viewed_by": user,  # This confirms which officer is looking at it
        "complaints": details
    }
@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("officer_session")
    return {"message": "Logged out successfully"}
=======
<<<<<<< HEAD
from fastapi import FastAPI, Response, HTTPException
import jwt
from datetime import datetime, timedelta
from fastapi import Cookie, Depends

# Import your custom files
import schema
import H1

app = FastAPI()
SECRET_KEY = "your_hackathon_secret_key"

def get_current_user(officer_session: str = Cookie(None)):
    if not officer_session:
        raise HTTPException(status_code=401, detail="Not logged in")

    try:
        payload = jwt.decode(officer_session, SECRET_KEY, algorithms=["HS256"])
        return payload["email"]
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

@app.post("/register-officer")
async def register(data: schema.RegisterRequest):
    success = H1.add_officer(data.email, data.password)
    if not success:
        raise HTTPException(status_code=400, detail="Email already exists")
    return {"message": "Officer registered successfully"}

@app.post("/login")
async def login(data: schema.LoginRequest, response: Response):
    user = H1.verify_officer(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"email": data.email, "exp": datetime.utcnow() + timedelta(hours=24)}, 
        SECRET_KEY, 
        algorithm="HS256"
    )

    response.set_cookie(key="officer_session", value=token, httponly=True ,samesite="lax")
    return {"status": "success", "user": data.email}
# -------- COMPLAINT --------
@app.post("/complaint")
async def complaint(data: schema.ComplaintRequest):
    result = H1.process_complaint(
        data.citizen_name,
        data.citizen_email,
        data.raw_text,
        data.category,
        data.district
    )
    return result


# -------- DASHBOARD --------
@app.get("/clusters")
def clusters(user=Depends(get_current_user)):
    return H1.get_clusters()


@app.get("/heatmap")
def heatmap(user=Depends(get_current_user)):
    return H1.get_heatmap()


@app.put("/complaint/{complaint_id}/status")
def update_status(complaint_id: int, status: str):
    return H1.update_complaint_status(complaint_id, status)
@app.get("/clusters/{cluster_id}/complaints")
async def cluster_details(cluster_id: int, user=Depends(get_current_user)):
    """
    Only logged-in officers can see the specific 
    complaints inside a cluster.
    """
    details = H1.get_complaints_by_cluster(cluster_id)
    
    if not details:
        raise HTTPException(status_code=404, detail="No complaints found for this cluster")
        
    return {
        "cluster_id": cluster_id,
        "viewed_by": user,  # This confirms which officer is looking at it
        "complaints": details
=======
from fastapi import FastAPI, Response, HTTPException
import jwt
from datetime import datetime, timedelta
from fastapi import Cookie, Depends

# Import your custom files
import schema
import H1

app = FastAPI()
SECRET_KEY = "your_hackathon_secret_key"

def get_current_user(officer_session: str = Cookie(None)):
    if not officer_session:
        raise HTTPException(status_code=401, detail="Not logged in")

    try:
        payload = jwt.decode(officer_session, SECRET_KEY, algorithms=["HS256"])
        return payload["email"]
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

@app.post("/register-officer")
async def register(data: schema.RegisterRequest):
    success = H1.add_officer(data.email, data.password)
    if not success:
        raise HTTPException(status_code=400, detail="Email already exists")
    return {"message": "Officer registered successfully"}

@app.post("/login")
async def login(data: schema.LoginRequest, response: Response):
    user = H1.verify_officer(data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"email": data.email, "exp": datetime.utcnow() + timedelta(hours=24)}, 
        SECRET_KEY, 
        algorithm="HS256"
    )

    response.set_cookie(key="officer_session", value=token, httponly=True ,samesite="lax")
    return {"status": "success", "user": data.email}
# -------- COMPLAINT --------
@app.post("/complaint")
async def complaint(data: schema.ComplaintRequest):
    result = H1.process_complaint(
        data.citizen_name,
        data.citizen_email,
        data.raw_text,
        data.category,
        data.district
    )
    return result


# -------- DASHBOARD --------
@app.get("/clusters")
def clusters(user=Depends(get_current_user)):
    return H1.get_clusters()


@app.get("/heatmap")
def heatmap(user=Depends(get_current_user)):
    return H1.get_heatmap()


@app.put("/complaint/{complaint_id}/status")
def update_status(complaint_id: int, status: str):
    return H1.update_complaint_status(complaint_id, status)
@app.get("/clusters/{cluster_id}/complaints")
async def cluster_details(cluster_id: int, user=Depends(get_current_user)):
    """
    Only logged-in officers can see the specific 
    complaints inside a cluster.
    """
    details = H1.get_complaints_by_cluster(cluster_id)
    
    if not details:
        raise HTTPException(status_code=404, detail="No complaints found for this cluster")
        
    return {
        "cluster_id": cluster_id,
        "viewed_by": user,  # This confirms which officer is looking at it
        "complaints": details
>>>>>>> fc41aca64f24f5c9b5e21b2bf8ccc7ab4882f74b
    }
>>>>>>> 018686aab8fbf5bb520e42656d7230c1d94851f3
