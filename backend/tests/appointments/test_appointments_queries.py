from flask.testing import FlaskClient
import pytest
import time_machine
from backend.appointments.constants import AppointmentStatus
from backend.appointments.queries import get_appointments_for_coach_in_range_query, get_appointments_for_user_query, get_open_appointments_query
from backend.appointments.models import Appointment
from backend.auth.constants import UserRole
from backend.auth.models import User
from datetime import datetime, timedelta, timezone
from backend.tests.factories.appointment_factory import AppointmentFactory
from backend.tests.factories.user_factory import UserFactory
from backend.types.query_opts import PaginationInfo, QueryOpts

def test_get_appointments_for_coach_in_range_query(client: FlaskClient, test_coach: User):
    appointment_1 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 9, 0, 0))
    appointment_2 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 11, 0, 0))
    appointment_3 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 13, 0, 0))

    appointments = get_appointments_for_coach_in_range_query(test_coach.id, datetime(2024, 1, 1, 9, 0, 0), datetime(2024, 1, 1, 13, 0, 0))
    assert len(appointments) == 1
    assert appointment_1 not in appointments
    assert appointment_2 in appointments
    assert appointment_3 not in appointments

    appointments = get_appointments_for_coach_in_range_query(test_coach.id, datetime(2024, 1, 1, 8, 59, 59), datetime(2024, 1, 1, 13, 0, 1))
    assert len(appointments) == 3
    assert appointment_1 in appointments
    assert appointment_2 in appointments
    assert appointment_3 in appointments

@time_machine.travel(datetime(2024, 1, 1, 10, 0, 0).replace(tzinfo=timezone.utc), tick=False)
def test_get_open_appointments_query(test_coach: User, test_student: User):
    test_coach_2 = UserFactory(role=UserRole.COACH).create()
    
    appointment_1 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 9, 0, 0)).create()
    appointment_2 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 11, 0, 0)).create()    
    appointment_3 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 13, 0, 0)).create()    
    appointment_4 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 15, 0, 0), status=AppointmentStatus.SCHEDULED, student_id=test_student.id).create()    
    appointment_5 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 2, 17, 0, 0)).create()    
    appointment_6 = AppointmentFactory(coach_id=test_coach_2.id, appointment_time=datetime(2024, 1, 1, 10, 0, 0)).create()  
    
    # Test not filtering by coach, appointments starting after now
    appointments, has_more = get_open_appointments_query(PaginationInfo())
    appointment_ids = [appt.id for appt in appointments]    
    assert len(appointments) == 4
    assert appointment_1.id not in appointment_ids
    assert appointment_2.id in appointment_ids
    assert appointment_3.id in appointment_ids
    assert appointment_4.id not in appointment_ids
    assert appointment_5.id in appointment_ids
    assert appointment_6.id in appointment_ids
    assert not has_more

    # Test filtering by coach, appointments starting after now
    appointments, has_more = get_open_appointments_query(PaginationInfo(), coach_id=test_coach.id)
    appointment_ids = [appt.id for appt in appointments]    
    assert len(appointments) == 3
    assert appointment_1.id not in appointment_ids
    assert appointment_2.id in appointment_ids
    assert appointment_3.id in appointment_ids
    assert appointment_4.id not in appointment_ids
    assert appointment_5.id in appointment_ids
    assert appointment_6.id not in appointment_ids
    assert not has_more

    # Test filtering after specific datetime
    appointments, has_more = get_open_appointments_query(PaginationInfo(), start_date_inclusive=datetime(2024, 1, 1, 13, 0, 0), coach_id=test_coach.id)
    appointment_ids = [appt.id for appt in appointments]    
    assert len(appointments) == 2
    assert appointment_1.id not in appointment_ids
    assert appointment_2.id not in appointment_ids
    assert appointment_3.id in appointment_ids
    assert appointment_4.id not in appointment_ids
    assert appointment_5.id in appointment_ids
    assert appointment_6.id not in appointment_ids
    assert not has_more

    # Test filtering after specific datetime before now
    appointments, has_more = get_open_appointments_query(PaginationInfo(), start_date_inclusive=datetime(2024, 1, 1, 9, 0, 0), coach_id=test_coach.id)
    appointment_ids = [appt.id for appt in appointments]    
    assert len(appointments) == 4
    assert appointment_1.id in appointment_ids
    assert appointment_2.id in appointment_ids
    assert appointment_3.id in appointment_ids
    assert appointment_4.id not in appointment_ids
    assert appointment_5.id in appointment_ids
    assert appointment_6.id not in appointment_ids
    assert not has_more

def test_get_appointments_for_user_query(client: FlaskClient, test_coach: User, test_student: User, test_root: User):
    test_coach_2 = UserFactory(role=UserRole.COACH).create()
    test_student_2 = UserFactory(role=UserRole.STUDENT).create()

    appointment_1 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 9, 0, 0)).create()
    appointment_2 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 11, 0, 0)).create()
    appointment_3 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 13, 0, 0)).create()
    appointment_4 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 15, 0, 0), status=AppointmentStatus.SCHEDULED, student_id=test_student.id).create()
    appointment_5 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 2, 17, 0, 0)).create()
    appointment_6 = AppointmentFactory(coach_id=test_coach_2.id, appointment_time=datetime(2024, 1, 1, 10, 0, 0)).create()
    appointment_7 = AppointmentFactory(coach_id=test_root.id, appointment_time=datetime(2024, 1, 1, 10, 0, 0), status=AppointmentStatus.SCHEDULED, student_id=test_student.id).create()
    appointment_8 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 10, 0, 0), status=AppointmentStatus.SCHEDULED, student_id=test_root.id).create()
    appointment_9 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 15, 0, 0), status=AppointmentStatus.SCHEDULED, student_id=test_student_2.id).create()

    # Test as student
    appointments, has_more = get_appointments_for_user_query(test_student, QueryOpts())
    appointment_ids = [appt.id for appt in appointments]    
    assert len(appointments) == 2
    assert appointment_1.id not in appointment_ids
    assert appointment_2.id not in appointment_ids
    assert appointment_3.id not in appointment_ids
    assert appointment_4.id in appointment_ids
    assert appointment_5.id not in appointment_ids
    assert appointment_6.id not in appointment_ids
    assert appointment_7.id in appointment_ids
    assert appointment_8.id not in appointment_ids
    assert appointment_9.id not in appointment_ids
    assert not has_more

    # Test as coach
    appointments, has_more = get_appointments_for_user_query(test_coach, QueryOpts())
    appointment_ids = [appt.id for appt in appointments]    
    assert len(appointments) == 7
    assert appointment_1.id in appointment_ids
    assert appointment_2.id in appointment_ids
    assert appointment_3.id in appointment_ids
    assert appointment_4.id in appointment_ids
    assert appointment_5.id in appointment_ids
    assert appointment_6.id not in appointment_ids
    assert appointment_7.id not in appointment_ids
    assert appointment_8.id in appointment_ids
    assert appointment_9.id in appointment_ids
    assert not has_more

    # Test as root, forget to specify as_student
    with pytest.raises(ValueError):
        get_appointments_for_user_query(test_root, QueryOpts())

    # Test as root, specify as_student
    appointments, has_more = get_appointments_for_user_query(test_root, QueryOpts(), as_student=True)
    appointment_ids = [appt.id for appt in appointments]    
    assert len(appointments) == 1
    assert appointment_1.id not in appointment_ids
    assert appointment_2.id not in appointment_ids
    assert appointment_3.id not in appointment_ids
    assert appointment_4.id not in appointment_ids
    assert appointment_5.id not in appointment_ids
    assert appointment_6.id not in appointment_ids
    assert appointment_7.id not in appointment_ids
    assert appointment_8.id in appointment_ids
    assert not has_more

    # Test as root, not as student
    appointments, has_more = get_appointments_for_user_query(test_root, QueryOpts(), as_student=False)
    appointment_ids = [appt.id for appt in appointments]    
    assert len(appointments) == 1
    assert appointment_1.id not in appointment_ids
    assert appointment_2.id not in appointment_ids
    assert appointment_3.id not in appointment_ids
    assert appointment_4.id not in appointment_ids
    assert appointment_5.id not in appointment_ids
    assert appointment_6.id not in appointment_ids
    assert appointment_7.id in appointment_ids
    assert appointment_8.id not in appointment_ids
    assert not has_more
