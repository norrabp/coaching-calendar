import factory

from backend.appointments.constants import AppointmentStatus
from backend.appointments.models import Appointment
from backend.extensions.extensions import db
from backend.tests.factories.user_factory import UserFactory


class AppointmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Appointment
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    coach_id = factory.SubFactory(UserFactory)
    appointment_time = factory.Faker(
        "date_time_between", start_date="-30d", end_date="now"
    )
    status = AppointmentStatus.OPEN
    student_id = None
    notes = None
    student_satisfaction = None
