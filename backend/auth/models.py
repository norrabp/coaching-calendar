from datetime import datetime
from backend.auth.constants import UserRole
from werkzeug.security import generate_password_hash, check_password_hash
from backend.extensions.extensions import db
from backend.database.db_model import Model

class User(Model):
    __tablename__ = 'users'
    
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.STUDENT, nullable=False)

    def __init__(self, username: str, email: str, phone_number: str, role: UserRole):
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.role = role
    
    def set_password(self, password: str):
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            c.name: getattr(self, c.name).isoformat()
            if isinstance(getattr(self, c.name), datetime)
            else getattr(self, c.name)
            for c in self.__table__.columns if c.name != 'password_hash'
        }
