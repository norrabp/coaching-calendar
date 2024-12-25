from flask.testing import FlaskClient
from backend.appointments.queries import get_appointments_for_coach_in_range
from backend.appointments.models import Appointment
from backend.auth.models import User
from datetime import datetime, timedelta
from backend.tests.factories.appointment_factory import AppointmentFactory

def test_get_appointments_for_coach_in_range(client: FlaskClient, test_coach: User):
    appointment_1 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 9, 0, 0))
    appointment_2 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 11, 0, 0))
    appointment_3 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 13, 0, 0))

    appointments = get_appointments_for_coach_in_range(test_coach.id, datetime(2024, 1, 1, 9, 0, 0), datetime(2024, 1, 1, 13, 0, 0))
    assert len(appointments) == 1
    assert appointment_1 not in appointments
    assert appointment_2 in appointments
    assert appointment_3 not in appointments

    appointments = get_appointments_for_coach_in_range(test_coach.id, datetime(2024, 1, 1, 8, 59, 59), datetime(2024, 1, 1, 13, 0, 1))
    assert len(appointments) == 3
    assert appointment_1 in appointments
    assert appointment_2 in appointments
    assert appointment_3 in appointments
