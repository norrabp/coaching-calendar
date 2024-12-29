

from datetime import datetime, timezone

from flask.testing import FlaskClient
import time_machine
from backend.appointments.constants import DEFAULT_APPOINTMENT_SLOTS, AppointmentStatus
from backend.appointments.models import Appointment
from backend.auth.models import User
from backend.tests.factories.appointment_factory import AppointmentFactory
from backend.tests.factories.user_factory import UserFactory
from backend.auth.constants import UserRole
from backend.types.query_opts import PaginationInfo


def test_create_appointment(client: FlaskClient, test_coach: User, coach_auth_headers: dict):
    assert Appointment.query.count() == 0
    response = client.post('/appointments', headers=coach_auth_headers, json={
        'coach_id': test_coach.id,
        'appointment_time': datetime(2024, 1, 1, 11, 0, 0).isoformat(),
        'status': AppointmentStatus.OPEN,
        'student_id': None,
        'notes': None,
        'student_satisfaction': None
    })
    assert response.status_code == 201
    assert Appointment.query.count() == 1
    assert Appointment.query.first().coach_id == test_coach.id
    assert Appointment.query.first().appointment_time == datetime(2024, 1, 1, 11, 0, 0)
    assert Appointment.query.first().status == AppointmentStatus.OPEN
    assert Appointment.query.first().student_id is None
    assert Appointment.query.first().notes is None
    assert Appointment.query.first().student_satisfaction is None

def test_create_appointment_invalid_time(client: FlaskClient, test_coach: User, coach_auth_headers: dict):
    assert Appointment.query.count() == 0
    response = client.post('/appointments', headers=coach_auth_headers, json={
        'coach_id': test_coach.id,
        'appointment_time': datetime(2024, 1, 1, 11, 0, 0).isoformat(),
        'status': AppointmentStatus.OPEN,
        'student_id': None,
        'notes': None,
        'student_satisfaction': None
    })
    assert response.status_code == 201
    assert Appointment.query.count() == 1
    assert Appointment.query.first().coach_id == test_coach.id
    assert Appointment.query.first().appointment_time == datetime(2024, 1, 1, 11, 0, 0)
    assert Appointment.query.first().status == AppointmentStatus.OPEN
    assert Appointment.query.first().student_id is None
    assert Appointment.query.first().notes is None
    assert Appointment.query.first().student_satisfaction is None

    response = client.post('/appointments', headers=coach_auth_headers, json={
        'coach_id': test_coach.id,
        'appointment_time': datetime(2024, 1, 1, 11, 0, 0).isoformat(),
        'status': AppointmentStatus.OPEN,
        'student_id': None,
        'notes': None,
        'student_satisfaction': None
    })
    assert response.status_code == 400
    assert Appointment.query.count() == 1

    response = client.post('/appointments', headers=coach_auth_headers, json={
        'coach_id': test_coach.id,
        'appointment_time': datetime(2024, 1, 1, 10, 0, 0).isoformat(),
        'status': AppointmentStatus.OPEN,
        'student_id': None,
        'notes': None,
        'student_satisfaction': None
    })
    assert response.status_code == 400
    assert Appointment.query.count() == 1

    response = client.post('/appointments', headers=coach_auth_headers, json={
        'coach_id': test_coach.id,
        'appointment_time': datetime(2024, 1, 1, 12, 0, 0).isoformat(),
        'status': AppointmentStatus.OPEN,
        'student_id': None,
        'notes': None,
        'student_satisfaction': None
    })
    assert response.status_code == 400
    assert Appointment.query.count() == 1

def test_create_appointment_invalid_completion(client: FlaskClient, test_coach: User, coach_auth_headers: dict):
    assert Appointment.query.count() == 0
    response = client.post('/appointments', headers=coach_auth_headers, json={
        'coach_id': test_coach.id,
        'appointment_time': datetime(2024, 1, 1, 11, 0, 0).isoformat(),
        'status': AppointmentStatus.COMPLETED,
        'student_id': None,
        'notes': None,
        'student_satisfaction': None
    })
    assert response.status_code == 400
    assert Appointment.query.count() == 0

def test_auth_headers_valid(client, coach_auth_headers):
    response = client.get('/auth/me', headers=coach_auth_headers)
    print(response)
    assert response.status_code == 200


@time_machine.travel(datetime(2024, 1, 1, 10, 0, 0).replace(tzinfo=timezone.utc), tick=False)
def test_get_open_appointments(client: FlaskClient, test_student: User, test_coach: User):
    # Need to log in now because of time travel
    response = client.post('/auth/login', json={
        'email': 'unittestcoach@example.com',
        'password': 'TestCoach@2024Secure!'
    })
    token = response.json['access_token']
    coach_auth_headers = {'Authorization': f'Bearer {token}'}

    response = client.post('/auth/login', json={
        'email': 'unittesting@example.com',
        'password': 'TestUser@2024Secure!'
    })
    token = response.json['access_token']
    student_auth_headers = {'Authorization': f'Bearer {token}'}

    test_coach_2 = UserFactory(role=UserRole.COACH).create()
    
    appointment_1 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 9, 0, 0)).create()
    appointment_2 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 11, 0, 0)).create()    
    appointment_3 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 13, 0, 0)).create()    
    appointment_4 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 15, 0, 0), status=AppointmentStatus.SCHEDULED, student_id=test_student.id).create()    
    appointment_5 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 2, 17, 0, 0)).create()    
    appointment_6 = AppointmentFactory(coach_id=test_coach_2.id, appointment_time=datetime(2024, 1, 2, 10, 0, 0)).create()  
    
    
    # Coaches can't view open appointments
    response = client.post('/appointments/open', headers=coach_auth_headers, json={})
    assert response.status_code == 403
    assert response.json == {'error': 'You are not authorized to view open appointments'}


    # Students can view open appointments
    response = client.post('/appointments/open', headers=student_auth_headers, json={})
    assert response.status_code == 200
    assert len(response.json['appointments']) == 4
    appointment_ids = [appt['id'] for appt in response.json['appointments']]
    assert str(appointment_1.id) not in appointment_ids
    assert str(appointment_2.id) in appointment_ids
    assert str(appointment_3.id) in appointment_ids
    assert str(appointment_4.id) not in appointment_ids
    assert str(appointment_5.id) in appointment_ids
    assert str(appointment_6.id) in appointment_ids

    # Test filtering after specific datetime
    response = client.post('/appointments/open', headers=student_auth_headers, json={
        'start_time': datetime(2024, 1, 1, 13, 0, 0).replace(tzinfo=timezone.utc).isoformat()
    })
    assert response.status_code == 200
    # assert len(response.json['appointments']) == 3
    appointment_ids = [appt['id'] for appt in response.json['appointments']]
    assert str(appointment_1.id) not in appointment_ids
    assert str(appointment_2.id) not in appointment_ids
    assert str(appointment_3.id) in appointment_ids
    assert str(appointment_4.id) not in appointment_ids
    assert str(appointment_5.id) in appointment_ids
    assert str(appointment_6.id) in appointment_ids

    # Test filtering by coach
    response = client.post('/appointments/open', headers=student_auth_headers, json={
        'coach_id': test_coach.id
    })
    assert response.status_code == 200
    assert len(response.json['appointments']) == 3
    appointment_ids = [appt['id'] for appt in response.json['appointments']]
    assert str(appointment_1.id) not in appointment_ids
    assert str(appointment_2.id) in appointment_ids
    assert str(appointment_3.id) in appointment_ids
    assert str(appointment_4.id) not in appointment_ids
    assert str(appointment_5.id) in appointment_ids
    assert str(appointment_6.id) not in appointment_ids

    # Test pagination
    response = client.post('/appointments/open', headers=student_auth_headers, json={
        'pagination_info': {
            'page': 1,
            'page_size': 2
        }
    })
    assert response.status_code == 200
    assert len(response.json['appointments']) == 2
    appointment_ids = [appt['id'] for appt in response.json['appointments']]
    assert str(appointment_1.id) not in appointment_ids
    assert str(appointment_2.id) in appointment_ids
    assert str(appointment_3.id) in appointment_ids
    assert str(appointment_4.id) not in appointment_ids
    assert str(appointment_5.id) not in appointment_ids
    assert str(appointment_6.id) not in appointment_ids
    assert response.json['has_next_page'] is True

    response = client.post('/appointments/open', headers=student_auth_headers, json={
        'pagination_info': {
            'page': 2,
            'page_size': 2
        }
    })
    assert response.status_code == 200
    assert len(response.json['appointments']) == 2
    appointment_ids = [appt['id'] for appt in response.json['appointments']]
    assert str(appointment_1.id) not in appointment_ids
    assert str(appointment_2.id) not in appointment_ids
    assert str(appointment_3.id) not in appointment_ids
    assert str(appointment_4.id) not in appointment_ids
    assert str(appointment_5.id) in appointment_ids
    assert str(appointment_6.id) in appointment_ids
    assert response.json['has_next_page'] is False


def test_get_my_appointments(client: FlaskClient, test_student: User, test_coach: User, test_root: User, student_auth_headers: dict, coach_auth_headers: dict, root_auth_headers: dict):
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
    response = client.post('/appointments/my', headers=student_auth_headers, json={})
    assert response.status_code == 200
    appointment_ids = [appt['id'] for appt in response.json['appointments']]    
    assert len(response.json['appointments']) == 2
    assert str(appointment_1.id) not in appointment_ids
    assert str(appointment_2.id) not in appointment_ids
    assert str(appointment_3.id) not in appointment_ids
    assert str(appointment_4.id) in appointment_ids
    assert str(appointment_5.id) not in appointment_ids
    assert str(appointment_6.id) not in appointment_ids
    assert str(appointment_7.id) in appointment_ids
    assert str(appointment_8.id) not in appointment_ids
    assert str(appointment_9.id) not in appointment_ids
    assert not response.json['has_next_page']

    # Test as coach
    response = client.post('/appointments/my', headers=coach_auth_headers, json={})
    assert response.status_code == 200
    appointment_ids = [appt['id'] for appt in response.json['appointments']]    
    assert len(response.json['appointments']) == 7
    assert str(appointment_1.id) in appointment_ids
    assert str(appointment_2.id) in appointment_ids
    assert str(appointment_3.id) in appointment_ids
    assert str(appointment_4.id) in appointment_ids
    assert str(appointment_5.id) in appointment_ids
    assert str(appointment_6.id) not in appointment_ids
    assert str(appointment_7.id) not in appointment_ids
    assert str(appointment_8.id) in appointment_ids
    assert str(appointment_9.id) in appointment_ids
    assert not response.json['has_next_page']

    # Test as root, forget to specify as_student
    response = client.post('/appointments/my', headers=root_auth_headers, json={})
    assert response.status_code == 400
    assert response.json == {'error': 'Must view appointments as a student or coach'}

    # Test as root, specify as_student
    response = client.post('/appointments/my', headers=root_auth_headers, json={
        'as_student': True
    })
    assert response.status_code == 200
    appointment_ids = [appt['id'] for appt in response.json['appointments']]    
    assert len(response.json['appointments']) == 1
    assert str(appointment_1.id) not in appointment_ids
    assert str(appointment_2.id) not in appointment_ids
    assert str(appointment_3.id) not in appointment_ids
    assert str(appointment_4.id) not in appointment_ids
    assert str(appointment_5.id) not in appointment_ids
    assert str(appointment_6.id) not in appointment_ids
    assert str(appointment_7.id) not in appointment_ids
    assert str(appointment_8.id) in appointment_ids
    assert not response.json['has_next_page']

    # Test as root, not as student
    response = client.post('/appointments/my', headers=root_auth_headers, json={
        'as_student': False
    })
    assert response.status_code == 200
    appointment_ids = [appt['id'] for appt in response.json['appointments']]    
    assert len(response.json['appointments']) == 1
    assert str(appointment_1.id) not in appointment_ids
    assert str(appointment_2.id) not in appointment_ids
    assert str(appointment_3.id) not in appointment_ids
    assert str(appointment_4.id) not in appointment_ids
    assert str(appointment_5.id) not in appointment_ids
    assert str(appointment_6.id) not in appointment_ids
    assert str(appointment_7.id) in appointment_ids
    assert str(appointment_8.id) not in appointment_ids
    assert not response.json['has_next_page']

def test_get_appointment_by_id(client: FlaskClient, test_student: User, test_coach: User, test_root: User, student_auth_headers: dict, coach_auth_headers: dict, root_auth_headers: dict):
    open_appointment = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 9, 0, 0)).create()
    scheduled_appointment = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 11, 0, 0), status=AppointmentStatus.SCHEDULED, student_id=test_student.id).create()
    
    

    # Test existing appointment
    response = client.get(f'/appointments/{open_appointment.id}', headers=student_auth_headers)
    assert response.status_code == 200
    assert response.json['appointment']['id'] == str(open_appointment.id)
    assert response.json['appointment']['coach_id'] == str(open_appointment.coach_id)
    assert response.json['appointment']['appointment_time'] == open_appointment.appointment_time.isoformat()
    assert response.json['appointment']['status'] == open_appointment.status.value
    assert response.json['appointment']['student_id'] == open_appointment.student_id
    assert response.json['appointment']['notes'] == open_appointment.notes
    assert response.json['appointment']['student_satisfaction'] == open_appointment.student_satisfaction
    assert 'coach_username' in response.json['appointment']
    assert 'student_username' not in response.json['appointment']
    assert 'coach_phone' not in response.json['appointment']
    assert 'student_phone' not in response.json['appointment']

    # Test scheduled appointment
    response = client.get(f'/appointments/{scheduled_appointment.id}', headers=student_auth_headers)
    assert response.status_code == 200
    assert response.json['appointment']['id'] == str(scheduled_appointment.id)
    assert response.json['appointment']['coach_id'] == str(scheduled_appointment.coach_id)
    assert response.json['appointment']['appointment_time'] == scheduled_appointment.appointment_time.isoformat()
    assert response.json['appointment']['status'] == scheduled_appointment.status.value
    assert response.json['appointment']['student_id'] == str(scheduled_appointment.student_id)
    assert response.json['appointment']['notes'] == scheduled_appointment.notes
    assert response.json['appointment']['student_satisfaction'] == scheduled_appointment.student_satisfaction
    assert 'coach_username' in response.json['appointment']
    assert 'student_username' in response.json['appointment']
    assert 'coach_phone' in response.json['appointment']
    assert 'student_phone' in response.json['appointment']


    # Test non-existent appointment
    deleted_id = open_appointment.id
    open_appointment.delete(hard_delete=True)

    response = client.get(f'/appointments/{deleted_id}', headers=student_auth_headers)
    assert response.status_code == 404

def test_update_appointment(client: FlaskClient, test_student: User, test_coach: User, test_root: User, student_auth_headers: dict, coach_auth_headers: dict, root_auth_headers: dict):
    # Create appointment
    response = client.post('/appointments', headers=coach_auth_headers, json={
        'coach_id': test_coach.id,
        'appointment_time': datetime(2024, 1, 1, 9, 0, 0).isoformat(),
        'status': AppointmentStatus.OPEN,
        'student_id': None,
        'notes': None,
        'student_satisfaction': None
    })
    assert response.status_code == 201
    appointment_id = response.json['appointment']['id']
    appointment = Appointment.query.get(appointment_id)
    assert appointment.status == AppointmentStatus.OPEN
    assert appointment.student_id is None
    assert appointment.notes is None
    assert appointment.student_satisfaction is None

    # Attempt to update open appointment with student, student satisfaction, or notes
    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'student_id': test_student.id,
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Appointment cannot be open with a student'}

    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'student_satisfaction': 1,
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Appointment cannot be open with student satisfaction'}

    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'notes': 'test',
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Appointment cannot be open with notes'}

    # Attempt to schedule or complete without student
    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'status': AppointmentStatus.SCHEDULED.value,
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Appointment must be completed or scheduled with a student'}

    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'status': AppointmentStatus.COMPLETED.value,
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Appointment must be completed or scheduled with a student'}

    # Attempt to assign coach as student
    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'status': AppointmentStatus.SCHEDULED.value,
        'student_id': test_coach.id,
    })
    assert response.status_code == 400
    assert response.json == {'error': 'User is not a student'}

    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'status': AppointmentStatus.COMPLETED.value,
        'student_id': test_coach.id,
        'student_satisfaction': 1,
        'notes': 'test',
    })
    assert response.status_code == 400
    assert response.json == {'error': 'User is not a student'}

    # Attempt to update appointment with student satisfaction
    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'status': AppointmentStatus.SCHEDULED.value,
        'student_id': test_student.id,
        'notes': 'test',
        'student_satisfaction': 1
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Appointment cannot be scheduled with student satisfaction'}

    # Schedule appointment with student
    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'status': AppointmentStatus.SCHEDULED,
        'student_id': test_student.id,
    })
    assert response.status_code == 200
    appointment = Appointment.query.get(appointment_id)
    assert appointment.status == AppointmentStatus.SCHEDULED
    assert appointment.student_id == test_student.id
    assert appointment.notes is None
    assert appointment.student_satisfaction is None

    # Attempt to complete appointment without notes
    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'status': AppointmentStatus.COMPLETED.value,
        'student_satisfaction': 1,
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Appointment must be completed with notes'}

    # Update notes for appointment
    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'notes': 'test',
    })
    assert response.status_code == 200
    appointment = Appointment.query.get(appointment_id)
    assert appointment.status == AppointmentStatus.SCHEDULED
    assert appointment.student_id == test_student.id
    assert appointment.notes == 'test'
    assert appointment.student_satisfaction is None

    # Attempt to complete appointment without student satisfaction
    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'status': AppointmentStatus.COMPLETED.value,
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Appointment must be completed with student satisfaction'}

    # Attempt to complete appointment with invalid student satisfaction
    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'status': AppointmentStatus.COMPLETED.value,
        'student_satisfaction': 6,
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Student satisfaction must be between 1 and 5'}

    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'status': AppointmentStatus.COMPLETED.value,
        'student_satisfaction': 0,
    })
    assert response.status_code == 400
    assert response.json == {'error': 'Student satisfaction must be between 1 and 5'}

    # Complete appointment with student satisfaction
    response = client.post(f'/appointments/{appointment_id}', headers=coach_auth_headers, json={
        'status': AppointmentStatus.COMPLETED.value,
        'student_satisfaction': 1,
        'notes': 'test',
    })
    assert response.status_code == 200
    appointment = Appointment.query.get(appointment_id)
    assert appointment.status == AppointmentStatus.COMPLETED
    assert appointment.student_id == test_student.id
    assert appointment.notes == 'test'
    assert appointment.student_satisfaction == 1

def test_get_available_slots(client: FlaskClient, test_coach: User, test_student: User, coach_auth_headers: dict, student_auth_headers: dict):
    test_coach_2 = UserFactory(role=UserRole.COACH).create()

    # Test as student
    response = client.post('/appointments/available-slots', headers=student_auth_headers, json={
        'start_time': datetime(2024, 1, 1, 9, 0, 0).isoformat(),
    })
    assert response.status_code == 403
    assert response.json == {'error': 'You are not authorized to view available slots'}

    # Test as coach
    response = client.post('/appointments/available-slots', headers=coach_auth_headers, json={
        'start_time': datetime(2024, 1, 1, 8, 0, 0).isoformat(),
    })
    assert response.status_code == 200
    assert len(DEFAULT_APPOINTMENT_SLOTS) == len(response.json['slots'])
    assert all([f"{slot.hour}:{slot.minute:02d}" in response.json['slots'] for slot in DEFAULT_APPOINTMENT_SLOTS])

    # Add some appointments

    # Overlapping
    appointment_1 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 9, 0, 0)).create()
    appointment_2 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 1, 11, 15, 0)).create()
    # Next day
    appointment_4 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 2, 13, 15, 0)).create()
    # Different coach
    appointment_5 = AppointmentFactory(coach_id=test_coach_2.id, appointment_time=datetime(2024, 1, 1, 13, 15, 0)).create()

    response = client.post('/appointments/available-slots', headers=coach_auth_headers, json={
        'start_time': datetime(2024, 1, 1, 7, 0, 0).isoformat(),
    })
    assert response.status_code == 200
    assert len(response.json['slots']) == 8
    assert "13:15" in response.json['slots']
    assert "13:30" in response.json['slots']
    assert "13:45" in response.json['slots']
    assert "14:00" in response.json['slots']
    assert "14:15" in response.json['slots']
    assert "14:30" in response.json['slots']
    assert "14:45" in response.json['slots']
    assert "15:00" in response.json['slots']

    appointment_6 = AppointmentFactory(coach_id=test_coach.id, appointment_time=datetime(2024, 1, 3, 11, 15, 0)).create()

    response = client.post('/appointments/available-slots', headers=coach_auth_headers, json={
        'start_time': datetime(2024, 1, 3, 7, 0, 0).isoformat(),
    })
    assert response.status_code == 200
    print(response.json['slots'])
    assert len(response.json['slots']) == 14
    assert "8:00" in response.json['slots']
    assert "8:15" in response.json['slots']
    assert "8:30" in response.json['slots']
    assert "8:45" in response.json['slots']
    assert "9:00" in response.json['slots']
    assert "9:15" in response.json['slots']
    assert "13:15" in response.json['slots']
    assert "13:30" in response.json['slots']
    assert "13:45" in response.json['slots']
    assert "14:00" in response.json['slots']
    assert "14:15" in response.json['slots']
    assert "14:30" in response.json['slots']
    assert "14:45" in response.json['slots']
    assert "15:00" in response.json['slots']

    response = client.post('/appointments/available-slots', headers=coach_auth_headers, json={
        'start_time': datetime(2024, 1, 3, 9, 0, 0).isoformat(),
    })
    assert response.status_code == 200
    assert len(response.json['slots']) == 10
    assert "9:00" in response.json['slots']
    assert "9:15" in response.json['slots']
    assert "13:15" in response.json['slots']
    assert "13:30" in response.json['slots']
    assert "13:45" in response.json['slots']
    assert "14:00" in response.json['slots']
    assert "14:15" in response.json['slots']
    assert "14:30" in response.json['slots']
    assert "14:45" in response.json['slots']
    assert "15:00" in response.json['slots']



   
