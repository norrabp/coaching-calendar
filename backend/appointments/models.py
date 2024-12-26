from backend.appointments.constants import AppointmentStatus
from backend.auth.models import User
from backend.extensions.extensions import db
from sqlalchemy.dialects.postgresql import UUID
from backend.database.db_model import Model
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, relationship

class Appointment(Model):
    __tablename__ = 'appointments'

    # Required fields
    coach_id: Mapped[UUID] = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    appointment_time: Mapped[datetime] = db.Column(db.DateTime)
    status: Mapped[AppointmentStatus] = db.Column(db.Enum(AppointmentStatus), default=AppointmentStatus.OPEN, nullable=False)
    
    # Optional fields
    student_id: Mapped[Optional[UUID]] = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)
    notes: Mapped[Optional[str]] = db.Column(db.Text, nullable=True)
    student_satisfaction: Mapped[Optional[int]] = db.Column(db.Integer, db.CheckConstraint('student_satisfaction >= 1 AND student_satisfaction <= 5'), nullable=True)

    # Relationships
    coach: Mapped[User] = relationship("User", foreign_keys=[coach_id], lazy='joined')
    student: Mapped[Optional[User]] = relationship("User", foreign_keys=[student_id], lazy='joined')

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
        base_dict = {
            c.name: getattr(self, c.name).isoformat()
            if isinstance(getattr(self, c.name), datetime)
            else getattr(self, c.name)
            for c in self.__table__.columns
        }
        base_dict['coach_username'] = self.coach.username
        if self.student:
            base_dict.update({
                'coach_phone': self.coach.phone_number,
                'student_username': self.student.username,
                'student_phone': self.student.phone_number
            })
        return base_dict