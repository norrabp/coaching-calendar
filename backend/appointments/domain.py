from backend.appointments.models import Appointment, AppointmentStatus
from backend.appointments.validation import validate_appointment_time, validate_appointment_completion
from backend.appointments.queries import create_appointment_query
from datetime import datetime
from typing import Optional
from uuid import UUID

def create_appointment(
    coach_id: UUID,
    appointment_time: datetime,
    status: AppointmentStatus = AppointmentStatus.OPEN,
    student_id: Optional[UUID] = None,
    notes: Optional[str] = None,
    student_satisfaction: Optional[int] = None
):
    validate_appointment_time(coach_id, appointment_time)
    if status == AppointmentStatus.COMPLETED:
        validate_appointment_completion(student_id, student_satisfaction, notes)
    return create_appointment_query(
        coach_id, appointment_time, status, student_id, notes, student_satisfaction
    )