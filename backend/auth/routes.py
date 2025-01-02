import logging

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from pydantic import ValidationError

from backend.app import db
from backend.auth.models import User
from backend.auth.queries import (
    create_user_query,
    get_user_by_email_query,
    get_user_by_id_query,
    get_user_by_username_query,
)
from backend.auth.request_models import LoginRequest, RegisterRequest

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = RegisterRequest.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    if get_user_by_username_query(data.username):
        return jsonify({"error": "Username already registered"}), 400

    if get_user_by_email_query(data.email):
        return jsonify({"error": "Email already registered"}), 400

    try:
        user = create_user_query(
            data.username, data.email, data.phone_number, data.role, data.password
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = LoginRequest.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    logger.info(f"Login attempt for email: {data.email}")

    user = get_user_by_email_query(data.email)

    if not user or not user.check_password(data.password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))
    logger.info(f"Login successful for user {user.id}")
    response = jsonify({"access_token": access_token, "user": user.to_dict()})
    return response, 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = get_user_by_id_query(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email})


@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users, has_next_page = User.get_list_and_paginate()
    return jsonify(
        {"users": [user.to_dict() for user in users], "has_next_page": has_next_page}
    )
