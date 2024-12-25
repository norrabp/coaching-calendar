from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from backend.appointments.request_models import CreateAppointmentRequest
from backend.appointments.domain import create_appointment
from flask_jwt_extended import jwt_required

appt_bp = Blueprint('appointments', __name__)

@appt_bp.route('/', methods=['POST'])
@jwt_required()
def create_appointment_api():
    try:
        data = CreateAppointmentRequest.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    
    if data.student_satisfaction and (data.student_satisfaction < 1 or data.student_satisfaction > 5):
        return jsonify({'error': 'Student satisfaction must be between 1 and 5'}), 400
    
    try:
        appointment = create_appointment(
            coach_id=data.coach_id,
            appointment_time=data.appointment_time,
            status=data.status,
            student_id=data.student_id,
            notes=data.notes,
        student_satisfaction=data.student_satisfaction
    )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'appointment': appointment.to_dict()}), 201
    

