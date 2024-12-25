from backend.appointments.models import Appointment
from backend.appointments.constants import AppointmentStatus
from datetime import datetime, timedelta
from uuid import UUID
from backend.appointments.queries import get_appointments_for_coach_in_range
from typing import Optional


def validate_appointment_completion(student_id: Optional[UUID], student_satisfaction: Optional[int], notes: Optional[str]) -> None:
    if student_id is None:
        raise ValueError('Appointment must be completed with a student')
    if student_satisfaction is None or student_satisfaction < 1 or student_satisfaction > 5:
        raise ValueError('Student satisfaction must be between 1 and 5')
    if notes is None:
        raise ValueError('Appointment must be completed with notes')


def validate_appointment_time(coach_id: UUID, appointment_time: datetime) -> None:
    """All appointments are 2 hours long, so we need to check less than 2 hours before and after the appointment time.
    We also need to check that the appointment time is at a quarter hour, and that there are no seconds or microseconds.
    """
    # Verify the time is at a quarter hour
    if appointment_time.minute % 15 != 0:
        raise ValueError('Appointment time must be at an exact quarter hour')
    # No seconds or microseconds
    if appointment_time.second != 0 or appointment_time.microsecond != 0 :
        raise ValueError('Appointment time must be at an exact quarter hour')
    # Check if the coach has an appointment at this time
    appointments = get_appointments_for_coach_in_range(coach_id, appointment_time - timedelta(hours=2), appointment_time + timedelta(hours=2))
    if len(appointments) > 0:
        raise ValueError('Coach already has an appointment at this time')
