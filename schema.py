from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
class ComplaintRequest(BaseModel):
    citizen_name: str
    citizen_email: str
    raw_text: str
    category: str
    district: str