from pydantic import BaseModel, field_validator
import re
from backend.auth.constants import UserRole

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    phone_number: str
    role: UserRole = UserRole.STUDENT

    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class LoginRequest(BaseModel):
    email: str
    password: str
