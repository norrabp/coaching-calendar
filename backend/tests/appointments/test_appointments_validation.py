from datetime import datetime
from wsgiref import validate

import pytest

from backend.appointments.constants import AppointmentStatus
from backend.appointments.validation import (
    validate_appointment_status,
    validate_appointment_time,
    validate_coach,
)
from backend.auth.models import User
from backend.tests.factories.appointment_factory import AppointmentFactory


def test_validate_appointment_time(test_coach: User):
    appointment_1 = AppointmentFactory(
        coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 9, 0, 0)
    )
    appointment_2 = AppointmentFactory(
        coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 13, 0, 0)
    )

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


def test_validate_appointment_status(
    test_coach: User, test_student: User, test_root: User
):
    # Validate open status
    validate_appointment_status(AppointmentStatus.OPEN, test_coach, None, None, None)
    with pytest.raises(ValueError):
        # Must be a coach
        validate_appointment_status(
            AppointmentStatus.OPEN, test_student, None, None, None
        )
    with pytest.raises(ValueError):
        # Cannot have a student
        validate_appointment_status(
            AppointmentStatus.OPEN, test_coach, test_student.id, None, None
        )
    with pytest.raises(ValueError):
        # Cannot have student satisfaction until completed
        validate_appointment_status(AppointmentStatus.OPEN, test_coach, None, 1, None)
    with pytest.raises(ValueError):
        # Cannot have notes until at least scheduled
        validate_appointment_status(
            AppointmentStatus.OPEN, test_coach, None, None, "test"
        )

    # Validate scheduled status
    validate_appointment_status(
        AppointmentStatus.SCHEDULED, test_coach, test_student.id, None, None
    )
    validate_appointment_status(
        AppointmentStatus.SCHEDULED, test_coach, test_root.id, None, "test"
    )
    # Students can schedule themselves!
    validate_appointment_status(
        AppointmentStatus.SCHEDULED, test_student, test_student.id, None, None
    )
    with pytest.raises(ValueError):
        # Must have a student
        validate_appointment_status(
            AppointmentStatus.SCHEDULED, test_coach, None, None, None
        )
    with pytest.raises(ValueError):
        # Cannot assign coach as student
        validate_appointment_status(
            AppointmentStatus.SCHEDULED, test_coach, test_coach.id, None, "test"
        )
    with pytest.raises(ValueError):
        # Cannot have student satisfaction until complete
        validate_appointment_status(
            AppointmentStatus.SCHEDULED, test_coach, None, 1, None
        )

    # Validate completed status
    validate_appointment_status(
        AppointmentStatus.COMPLETED, test_coach, test_student.id, 1, "test"
    )
    validate_appointment_status(
        AppointmentStatus.COMPLETED, test_coach, test_root.id, 1, "test"
    )
    with pytest.raises(ValueError):
        # Must be a coach
        validate_appointment_status(
            AppointmentStatus.COMPLETED, test_student, test_student.id, 1, "test"
        )
    with pytest.raises(ValueError):
        # Must have a student
        validate_appointment_status(
            AppointmentStatus.COMPLETED, test_coach, None, 1, "test"
        )
    with pytest.raises(ValueError):
        # Cannot assign coach as student
        validate_appointment_status(
            AppointmentStatus.COMPLETED, test_coach, test_coach.id, 1, "test"
        )
    with pytest.raises(ValueError):
        # Must have student satisfaction
        validate_appointment_status(
            AppointmentStatus.COMPLETED, test_coach, test_student.id, None, "test"
        )
    with pytest.raises(ValueError):
        # Must have notes
        validate_appointment_status(
            AppointmentStatus.COMPLETED, test_coach, test_student.id, 1, None
        )


def test_validate_coach(test_coach: User, test_student: User, test_root: User):
    validate_coach(test_coach.id)
    validate_coach(test_root.id)
    with pytest.raises(ValueError):
        validate_coach(test_student.id)
