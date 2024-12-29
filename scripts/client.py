from datetime import datetime
from typing import Dict, Optional
import requests

class FlaskAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def register(self, username: str, email: str, password: str, phone_number: str, role: str) -> Dict:
        endpoint = f"{self.base_url}/auth/register"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "phone_number": phone_number,
            "role": role
        }
        response = requests.post(endpoint, json=data)
        return response.json()

    def login(self, email: str, password: str) -> Dict:
        endpoint = f"{self.base_url}/auth/login"
        data = {
            "email": email,
            "password": password
        }
        response = requests.post(endpoint, json=data)
        if response.status_code == 200:
            self.token = response.json().get('access_token')
            self.headers['Authorization'] = f"Bearer {self.token}"
        return response.json()
    
    def clear_db(self) -> Dict:
        endpoint = f"{self.base_url}/api/clear-db"
        response = requests.post(endpoint, headers=self.headers)
        return response.json()

    def get_users(self) -> Dict:
        endpoint = f"{self.base_url}/api/users"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()

    def get_stats(self) -> Dict:
        endpoint = f"{self.base_url}/api/stats"
        response = requests.get(endpoint, headers=self.headers)
        return response.json()
    
    def create_appointment(self, coach_id: str, appointment_time: datetime, student_id: str = None, status: str = "OPEN", notes: str = None, student_satisfaction: int = None) -> Dict:
        endpoint = f"{self.base_url}/appointments"
        data = {
            "coach_id": coach_id,
            "appointment_time": appointment_time.isoformat(),
            "status": status,
            "notes": notes,
            "student_satisfaction": student_satisfaction,
            "student_id": student_id
        }
        response = requests.post(endpoint, json=data, headers=self.headers)
        return response.json()
