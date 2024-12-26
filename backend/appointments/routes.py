from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from backend.appointments.models import Appointment
from backend.appointments.queries import get_appointment_by_id_query, get_appointments_for_user_query, get_open_appointments_query
from backend.appointments.request_models import CreateAppointmentRequest, GetMyAppointmentsRequest, GetOpenAppointmentsRequest, UpdateAppointmentRequest
from backend.appointments.domain import create_appointment, update_appointment
from flask_jwt_extended import get_current_user, jwt_required

from backend.auth.constants import UserRole

appt_bp = Blueprint('appointments', __name__)

@appt_bp.route('/', methods=['POST'])
@jwt_required()
def create_appointment_api():
    try:
        data = CreateAppointmentRequest.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    
    current_user = get_current_user()
    if data.student_satisfaction and (data.student_satisfaction < 1 or data.student_satisfaction > 5):
        return jsonify({'error': 'Student satisfaction must be between 1 and 5'}), 400
    
    try:
        appointment = create_appointment(
            current_user,
            data.coach_id,
            data.appointment_time,
            data.status,
            data.student_id,
            data.notes,
            data.student_satisfaction
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'appointment': appointment.to_dict()}), 201

@appt_bp.route('/<appointment_id>', methods=['POST'])
@jwt_required()
def update_appointment_api(appointment_id: str):
    current_user = get_current_user()
    try:
        data = UpdateAppointmentRequest.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    
    appointment = get_appointment_by_id_query(appointment_id)
    try:
        appointment = update_appointment(appointment, current_user, data.student_id, data.status, data.notes, data.student_satisfaction)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    return jsonify({'appointment': appointment.to_dict()}), 200


@appt_bp.route('/open', methods=['POST'])
@jwt_required()
def get_open_appointments_api():
    try:
        data = GetOpenAppointmentsRequest.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    
    current_user = get_current_user()
    if current_user.role not in [UserRole.STUDENT, UserRole.ROOT]:
        return jsonify({'error': 'You are not authorized to view open appointments'}), 403
    
    appointments, has_next_page = get_open_appointments_query(data.pagination_info, start_date_inclusive=data.start_date, coach_id=data.coach_id)
    return jsonify({'appointments': [appointment.to_dict() for appointment in appointments], 'has_next_page': has_next_page}), 200
    

@appt_bp.route('/my', methods=['POST'])
@jwt_required()
def get_my_appointments_api():
    current_user = get_current_user()
    try:
        data = GetMyAppointmentsRequest.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    try:
        appointments, has_next_page = get_appointments_for_user_query(current_user, data.query_opts, as_student=data.as_student)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'appointments': [appointment.to_dict() for appointment in appointments], 'has_next_page': has_next_page}), 200

@appt_bp.route('/<appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment_api(appointment_id: str):
    appointment = get_appointment_by_id_query(appointment_id)
    return jsonify({'appointment': appointment.to_dict()}), 200