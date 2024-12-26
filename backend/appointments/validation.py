from backend.appointments.models import Appointment
from backend.appointments.constants import AppointmentStatus
from datetime import datetime, timedelta
from uuid import UUID
from backend.appointments.queries import get_appointments_for_coach_in_range_query
from typing import Optional, Union

from backend.auth.constants import UserRole
from backend.auth.models import User


def validate_coach(coach_id: Union[UUID, str]) -> User:
    coach = User.query.get_or_404(coach_id)
    if coach.role not in [UserRole.COACH, UserRole.ROOT]:
        raise ValueError('User is not a coach')
    return coach

def validate_student(student_id: Union[UUID, str]) -> User:
    student = User.query.get_or_404(student_id)
    if student.role not in [UserRole.STUDENT, UserRole.ROOT]:
        raise ValueError('User is not a student')
    return student

def validate_appointment_status(status: AppointmentStatus, current_user: User, student_id: Optional[Union[UUID, str]], student_satisfaction: Optional[int], notes: Optional[str]) -> None:
    if status in [AppointmentStatus.COMPLETED, AppointmentStatus.SCHEDULED]:
        if student_id is None:
            raise ValueError('Appointment must be completed or scheduled with a student')
        else:
            validate_student(student_id)
        if status == AppointmentStatus.COMPLETED:
            if current_user.role != UserRole.COACH:
                raise ValueError('Only coaches can complete appointments')
            if student_satisfaction is None:
                raise ValueError('Appointment must be completed with student satisfaction')
            elif student_satisfaction < 1 or student_satisfaction > 5:
                raise ValueError('Student satisfaction must be between 1 and 5')
            if notes is None:
                raise ValueError('Appointment must be completed with notes')
        else:
            if student_satisfaction is not None:
                raise ValueError('Appointment cannot be scheduled with student satisfaction')
    elif status == AppointmentStatus.OPEN:
        if current_user.role != UserRole.COACH:
            raise ValueError('Only coaches can open appointments')
        if student_id is not None:
            raise ValueError('Appointment cannot be open with a student')
        if student_satisfaction is not None:
            raise ValueError('Appointment cannot be open with student satisfaction')
        if notes is not None:
            raise ValueError('Appointment cannot be open with notes')


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
    appointments = get_appointments_for_coach_in_range_query(coach_id, appointment_time - timedelta(hours=2), appointment_time + timedelta(hours=2))
    if len(appointments) > 0:
        raise ValueError('Coach already has an appointment at this time')
