

from datetime import datetime

from flask.testing import FlaskClient
from backend.appointments.constants import AppointmentStatus
from backend.appointments.models import Appointment
from backend.auth.models import User


def test_create_appointment(client: FlaskClient, test_coach: User, coach_auth_headers: dict):
    assert Appointment.query.count() == 0
    response = client.post('/appointments/', headers=coach_auth_headers, json={
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
    response = client.post('/appointments/', headers=coach_auth_headers, json={
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

    response = client.post('/appointments/', headers=coach_auth_headers, json={
        'coach_id': test_coach.id,
        'appointment_time': datetime(2024, 1, 1, 11, 0, 0).isoformat(),
        'status': AppointmentStatus.OPEN,
        'student_id': None,
        'notes': None,
        'student_satisfaction': None
    })
    assert response.status_code == 400
    assert Appointment.query.count() == 1

    response = client.post('/appointments/', headers=coach_auth_headers, json={
        'coach_id': test_coach.id,
        'appointment_time': datetime(2024, 1, 1, 10, 0, 0).isoformat(),
        'status': AppointmentStatus.OPEN,
        'student_id': None,
        'notes': None,
        'student_satisfaction': None
    })
    assert response.status_code == 400
    assert Appointment.query.count() == 1

    response = client.post('/appointments/', headers=coach_auth_headers, json={
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
    response = client.post('/appointments/', headers=coach_auth_headers, json={
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
