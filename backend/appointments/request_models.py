from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.appointments.constants import AppointmentStatus

class CreateAppointmentRequest(BaseModel):
    student_id: Optional[str] = None
    coach_id: str
    appointment_time: datetime
    status: AppointmentStatus = AppointmentStatus.OPEN
    notes: Optional[str] = None
    student_satisfaction: Optional[int] = None