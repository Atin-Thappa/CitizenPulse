<<<<<<< HEAD
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
=======
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
>>>>>>> 018686aab8fbf5bb520e42656d7230c1d94851f3
    district: str