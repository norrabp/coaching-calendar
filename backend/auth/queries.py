from typing import List
from backend.auth.models import User
from backend.auth.constants import UserRole

def create_user_query(username: str, email: str, phone_number: str, role: UserRole, password: str, commit: bool = True) -> User:
    user = User(username=username, email=email, phone_number=phone_number, role=role)
    user.set_password(password)
    user.create(commit=commit)
    return user

def get_user_by_email_query(email: str) -> User:
    return User.get_list_query_obj(filter={'email': email}).first()

def get_user_by_username_query(username: str) -> User:
    return User.get_list_query_obj(filter={'username': username}).first()

def get_user_by_id_query(id: int) -> User:
    return User.get_list_query_obj(filter={'id': id}).first()

def get_all_coaches_query() -> List[User]:
    return User.get_list(filter={'role': UserRole.COACH})

def get_all_students_query() -> List[User]:
    return User.get_list(filter={'role': UserRole.STUDENT})