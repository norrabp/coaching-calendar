from backend.appointments.models import Appointment
from backend.appointments.constants import AppointmentStatus
from datetime import datetime
from typing import List, Optional

def create_appointment_query(
    coach_id: str,
    appointment_time: datetime,
    status: AppointmentStatus = AppointmentStatus.OPEN,
    student_id: Optional[str] = None,
    notes: Optional[str] = None,
    student_satisfaction: Optional[int] = None,
    commit: bool = True
) -> Appointment:
    appointment = Appointment(
        coach_id=coach_id,
        appointment_time=appointment_time,
        status=status,
        student_id=student_id,
        notes=notes,
        student_satisfaction=student_satisfaction
    )
    appointment.create(commit=commit)
    return appointment

def get_appointments_for_coach_in_range(coach_id: str, start_date_exclusive: datetime, end_date_exclusive: datetime) -> List[Appointment]:
    return Appointment.get_list({'coach_id': coach_id, 'appointment_time': {'$gt': start_date_exclusive, '$lt': end_date_exclusive}})
