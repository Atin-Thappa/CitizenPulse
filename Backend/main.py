
from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import jwt
from datetime import datetime, timedelta
from fastapi import Cookie, Depends
from dotenv import load_dotenv
import os

# Import your custom files
import schema
import codee

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SECRET_KEY = os.getenv("SECRET_KEY")

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
    success = codee.add_officer(data.email, data.password)
    if not success:
        raise HTTPException(status_code=400, detail="Email already exists")
    return {"message": "Officer registered successfully"}

@app.post("/login")
async def login(data: schema.LoginRequest, response: Response):
    user = codee.verify_officer(data.email, data.password)
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
    result = codee.process_complaint(
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
    return codee.get_clusters()


@app.get("/heatmap")
def heatmap(user=Depends(get_current_user)):
    return codee.get_heatmap()


@app.put("/complaint/{complaint_id}/status")
def update_status(complaint_id: int, status: str):
    return codee.update_complaint_status(complaint_id, status)
@app.get("/clusters/{cluster_id}/complaints")
async def cluster_details(cluster_id: int, user=Depends(get_current_user)):
    """
    Only logged-in officers can see the specific 
    complaints inside a cluster.
    """
    details = codee.get_complaints_by_cluster(cluster_id)
    
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
