from backend.appointments.models import Appointment, AppointmentStatus
from backend.appointments.validation import validate_appointment_time, validate_appointment_status, validate_coach, validate_student
from backend.appointments.queries import create_appointment_query, update_appointment_query
from datetime import datetime
from typing import Optional, Union
from uuid import UUID
from backend.types.modification import Modification, NOT_MODIFIED, get_modification
from backend.auth.models import User

def create_appointment(
    current_user: User,
    coach_id: UUID,
    appointment_time: datetime,
    status: AppointmentStatus = AppointmentStatus.OPEN,
    student_id: Optional[Union[UUID, str]] = None,
    notes: Optional[str] = None,
    student_satisfaction: Optional[int] = None
):
    validate_coach(coach_id)
    validate_appointment_time(coach_id, appointment_time)
    validate_appointment_status(status, current_user, student_id, student_satisfaction, notes)
    return create_appointment_query(
        coach_id, appointment_time, status, student_id, notes, student_satisfaction
    )

def update_appointment(
    appointment: Appointment,
    current_user: User,
    student_id: Modification[Union[UUID, str]] = NOT_MODIFIED,
    status: Modification[AppointmentStatus] = NOT_MODIFIED,
    notes: Modification[str] = NOT_MODIFIED,
    student_satisfaction: Modification[int] = NOT_MODIFIED
):
    student_id: Optional[Union[UUID, str]] = get_modification(student_id, appointment.student_id)
    status: Optional[AppointmentStatus] = get_modification(status, appointment.status)
    notes: Optional[str] = get_modification(notes, appointment.notes)
    student_satisfaction: Optional[int] = get_modification(student_satisfaction, appointment.student_satisfaction)
    validate_appointment_status(status, current_user, student_id, student_satisfaction, notes)
    return update_appointment_query(appointment, status, student_id, notes, student_satisfaction)   
