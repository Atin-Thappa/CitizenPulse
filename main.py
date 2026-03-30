from fastapi import FastAPI, Response, HTTPException
import jwt
from datetime import datetime, timedelta

# Import your custom files
import schema
import H1

app = FastAPI()
SECRET_KEY = "your_hackathon_secret_key"

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
def clusters():
    return H1.get_clusters()


@app.get("/heatmap")
def heatmap():
    return H1.get_heatmap()