from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.appointments.constants import AppointmentStatus
from backend.types.query_opts import PaginationInfo, QueryOpts
from backend.types.modification import Modification, NOT_MODIFIED

class CreateAppointmentRequest(BaseModel):
    student_id: Optional[str] = None
    coach_id: str
    appointment_time: datetime
    status: AppointmentStatus = AppointmentStatus.OPEN
    notes: Optional[str] = None
    student_satisfaction: Optional[int] = None

class GetOpenAppointmentsRequest(BaseModel):
    coach_id: Optional[str] = None
    start_time: Optional[datetime] = None
    pagination_info: PaginationInfo = PaginationInfo()
    
class GetMyAppointmentsRequest(BaseModel):
    query_opts: Optional[QueryOpts] = QueryOpts()
    as_student: Optional[bool] = None

class UpdateAppointmentRequest(BaseModel):
    student_id: Modification[str] = NOT_MODIFIED
    status: Modification[AppointmentStatus] = NOT_MODIFIED
    notes: Modification[str] = NOT_MODIFIED
    student_satisfaction: Modification[int] = NOT_MODIFIED

class GetAvailableSlotsRequest(BaseModel):
    start_time: datetime
    # TODO: Add end time when allowing locales outside UTC
