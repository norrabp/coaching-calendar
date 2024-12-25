from datetime import datetime
import pytest
from backend.appointments.validation import validate_appointment_completion, validate_appointment_time
from backend.auth.models import User
from backend.tests.factories.appointment_factory import AppointmentFactory

def test_validate_appointment_time(test_coach: User):
    appointment_1 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 9, 0, 0))
    appointment_2 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 13, 0, 0))

    # Valid time since between 2 slots
    validate_appointment_time(test_coach.id, datetime(2024, 1, 1, 11, 0, 0))

    # Invalid minutes
    with pytest.raises(ValueError):
        validate_appointment_time(test_coach.id, datetime(2024, 1, 2, 11, 1, 0))
    # Invalid seconds
    with pytest.raises(ValueError):
        validate_appointment_time(test_coach.id, datetime(2024, 1, 2, 11, 0, 1))
    # Invalid microseconds
    with pytest.raises(ValueError):
        validate_appointment_time(test_coach.id, datetime(2024, 1, 2, 11, 0, 0, 1))
    # Overlaps with an earlier appointment
    with pytest.raises(ValueError):
        validate_appointment_time(test_coach.id, datetime(2024, 1, 1, 9, 45, 0))
    # Overlaps with an later appointment
    with pytest.raises(ValueError):
        validate_appointment_time(test_coach.id, datetime(2024, 1, 1, 11, 15, 0))

