from datetime import datetime, time, timedelta
from typing import List, Optional, Union
from uuid import UUID

from backend.appointments.constants import DEFAULT_APPOINTMENT_SLOTS
from backend.appointments.models import Appointment, AppointmentStatus
from backend.appointments.queries import (
    create_appointment_query,
    get_existing_timeslots_by_datetime_query,
    update_appointment_query,
)
from backend.appointments.validation import (
    validate_appointment_status,
    validate_appointment_time,
    validate_coach,
    validate_student,
)
from backend.auth.models import User
from backend.types.modification import NOT_MODIFIED, Modification, get_modification


def create_appointment(
    current_user: User,
    coach_id: UUID,
    appointment_time: datetime,
    status: AppointmentStatus = AppointmentStatus.OPEN,
    student_id: Optional[Union[UUID, str]] = None,
    notes: Optional[str] = None,
    student_satisfaction: Optional[int] = None,
):
    validate_coach(coach_id)
    validate_appointment_time(coach_id, appointment_time)
    validate_appointment_status(
        status, current_user, student_id, student_satisfaction, notes
    )
    return create_appointment_query(
        coach_id, appointment_time, status, student_id, notes, student_satisfaction
    )


def update_appointment(
    appointment: Appointment,
    current_user: User,
    student_id: Modification[Union[UUID, str]] = NOT_MODIFIED,
    status: Modification[AppointmentStatus] = NOT_MODIFIED,
    notes: Modification[str] = NOT_MODIFIED,
    student_satisfaction: Modification[int] = NOT_MODIFIED,
):
    student_id: Optional[Union[UUID, str]] = get_modification(
        student_id, appointment.student_id
    )
    status: Optional[AppointmentStatus] = get_modification(status, appointment.status)
    notes: Optional[str] = get_modification(notes, appointment.notes)
    student_satisfaction: Optional[int] = get_modification(
        student_satisfaction, appointment.student_satisfaction
    )
    validate_appointment_status(
        status, current_user, student_id, student_satisfaction, notes
    )
    return update_appointment_query(
        appointment, status, student_id, notes, student_satisfaction
    )


def get_available_timeslots(coach: User, start_time: datetime) -> List[time]:
    """
    Get the available timeslots for a coach after a given start time.
    """
    existing_slots = get_existing_timeslots_by_datetime_query(coach, start_time)
    todays_slots = [
        datetime(
            start_time.year,
            start_time.month,
            start_time.day,
            slot.hour,
            slot.minute,
            0,
            0,
        )
        for slot in DEFAULT_APPOINTMENT_SLOTS
        if time(slot.hour, slot.minute, 0, 0) >= start_time.time()
    ]
    available_slots = []
    for slot in todays_slots:
        slot_start = slot
        slot_end = slot + timedelta(hours=2)
        available = True
        # Since all appointments are 2 hours long, we need to check if the slot overlaps with any existing appointments
        for existing_slot in existing_slots:
            if (
                slot_start >= existing_slot.appointment_time
                and slot_start < existing_slot.appointment_time + timedelta(hours=2)
            ):
                available = False
                break
            if (
                slot_end > existing_slot.appointment_time
                and slot_end <= existing_slot.appointment_time + timedelta(hours=2)
            ):
                available = False
                break
        if available:
            available_slots.append(slot)
    return available_slots
