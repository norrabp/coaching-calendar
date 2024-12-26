from uuid import UUID
from backend.appointments.models import Appointment
from backend.appointments.constants import AppointmentStatus
from datetime import datetime, timezone
from typing import List, Optional, Union

from backend.auth.constants import UserRole
from backend.auth.models import User
from backend.types.query_opts import FilterInfo, PaginationInfo, QueryOpts, SortInfo

def create_appointment_query(
    coach_id: str,
    appointment_time: datetime,
    status: AppointmentStatus = AppointmentStatus.OPEN,
    student_id: Optional[Union[str, UUID]] = None,
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

def update_appointment_query(
    appointment: Appointment, 
    status: AppointmentStatus = AppointmentStatus.OPEN,
    student_id: Optional[Union[str, UUID]] = None,
    notes: Optional[str] = None,
    student_satisfaction: Optional[int] = None,
    commit: bool = True
) -> Appointment:
    appointment.status = status
    appointment.student_id = student_id
    appointment.notes = notes
    appointment.student_satisfaction = student_satisfaction
    appointment.update(commit=commit)
    return appointment

def get_appointments_for_coach_in_range_query(coach_id: str, start_date_exclusive: datetime, end_date_exclusive: datetime) -> List[Appointment]:
    return Appointment.get_list({'coach_id': coach_id, 'appointment_time': {'$gt': start_date_exclusive, '$lt': end_date_exclusive}})

def get_open_appointments_query(pagination_info: PaginationInfo, start_date_inclusive: Optional[datetime] = None, coach_id: Optional[str] = None) -> tuple[List[Appointment], bool]:
    filter = {'status': AppointmentStatus.OPEN, 'appointment_time': {'$gte': start_date_inclusive or datetime.now(timezone.utc)}}
    if coach_id:
        filter['coach_id'] = coach_id
    return Appointment.get_list_and_paginate(filter, sort={'appointment_time': 'asc'}, pagination=pagination_info)

def get_appointments_for_user_query(user: User, query_opts: QueryOpts, as_student: Optional[bool] = None) -> tuple[List[Appointment], bool]:
    filter = query_opts.filter or {}
    if user.role == UserRole.STUDENT or (user.role == UserRole.ROOT and as_student is True):
        filter['student_id'] = user.id
    elif user.role == UserRole.COACH or (user.role == UserRole.ROOT and as_student is False):
        filter['coach_id'] = user.id
    else:
        raise ValueError('Must view appointments as a student or coach')
    return Appointment.get_list_and_paginate(filter=filter, sort=query_opts.sort, pagination=query_opts.pagination)

def get_appointment_by_id_query(appointment_id: Union[str, UUID]) -> Appointment:
    return Appointment.query.get_or_404(appointment_id)