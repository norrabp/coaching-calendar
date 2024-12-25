
from backend.appointments.constants import AppointmentStatus
from backend.extensions.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from backend.database.db_model import Model
from datetime import datetime
from typing import Optional

class Appointment(Model):
    __tablename__ = 'appointments'

    student_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)
    coach_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    appointment_time = db.Column(db.DateTime)
    status = db.Column(db.Enum(AppointmentStatus), default=AppointmentStatus.OPEN, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    student_satisfaction = db.Column(db.Integer, db.CheckConstraint('student_satisfaction >= 1 AND student_satisfaction <= 5'), nullable=True)

    def __init__(
        self, coach_id: UUID, appointment_time: datetime, status: AppointmentStatus = AppointmentStatus.OPEN,
        student_id: Optional[UUID] = None, notes: Optional[str] = None, student_satisfaction: Optional[int] = None
    ):
        self.student_id = student_id
        self.coach_id = coach_id
        self.appointment_time = appointment_time
        self.status = status
        self.notes = notes
        self.student_satisfaction = student_satisfaction

        
    def to_dict(self):
        return {
            c.name: getattr(self, c.name).isoformat()
            if isinstance(getattr(self, c.name), datetime)
            else getattr(self, c.name)
            for c in self.__table__.columns if c.name != 'password_hash'
        }