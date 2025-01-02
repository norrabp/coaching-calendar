import logging
import os

from flask import Flask, jsonify
from flask_migrate import Migrate

from backend.auth.constants import UserRole
from backend.auth.models import User
from backend.config.environment import CONFIG, ENVIRONMENT, Environment
from backend.extensions.extensions import celery, cors, db, jwt

# Initialize migrations
migrate = Migrate()


def create_app(config_class=CONFIG):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db, directory="backend/migrations")
    jwt.init_app(app)

    # Configure CORS with proper headers
    cors.init_app(
        app,
        resources={
            r"/*": {
                "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
                "methods": ["GET", "HEAD", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"],
                "allow_headers": ["Content-Type", "Authorization", "Cache-Control"],
                "expose_headers": ["Authorization", "Content-Type"],
                "supports_credentials": True,
                "send_wildcard": False,
            }
        },
    )

    # Additional error handlers for JWT
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error": "Invalid token", "message": str(error)}), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        app.logger.debug("Unauthorized")
        return jsonify({"error": "No token provided", "message": str(error)}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        app.logger.debug("Token expired")
        return {"error": "Token has expired"}, 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        app.logger.debug("Fresh token required")
        return {"error": "Fresh token required"}, 401

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id if hasattr(user, "id") else user

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        try:
            return User.query.filter_by(id=identity).one_or_none()
        except (ValueError, TypeError):
            return None

    celery.conf.update(app.config)

    # Initialize database
    with app.app_context():
        try:
            # Run migrations first
            from flask_migrate import upgrade

            upgrade(directory="backend/migrations")
            app.logger.info("Database migrations completed successfully")

            db.create_all()
            if ENVIRONMENT == Environment.DEVELOPMENT:
                # Create test user if it doesn't exist
                root_user = User.query.filter_by(role=UserRole.ROOT).first()
                if not root_user:
                    root_user = User(
                        username="root",
                        email="root@example.com",
                        phone_number="1234567890",
                        role=UserRole.ROOT,
                    )
                    root_user.set_password("Root@2024Secure!")
                    db.session.add(root_user)
                    db.session.commit()
                    app.logger.info("Root user created successfully")
                else:
                    app.logger.info("Root user already exists")
                coach_user = User.query.filter_by(role=UserRole.COACH).first()
                if not coach_user:
                    coach_user = User(
                        username="Jim Harbaugh",
                        email="jimharbaugh@gmail.com",
                        phone_number="1234567890",
                        role=UserRole.COACH,
                    )
                    coach_user.set_password("bad_pass")
                    db.session.add(coach_user)
                    db.session.commit()
                    app.logger.info("Coach user created successfully")
                else:
                    app.logger.info("Coach user already exists")
                student_user = User.query.filter_by(role=UserRole.STUDENT).first()
                if not student_user:
                    student_user = User(
                        username="JJ McCarthy",
                        email="jjmccarthy@gmail.com",
                        phone_number="1234567890",
                        role=UserRole.STUDENT,
                    )
                    student_user.set_password("bad_pass")
                    db.session.add(student_user)
                    db.session.commit()
                    app.logger.info("Student user created successfully")
                else:
                    app.logger.info("Student user already exists")
        except Exception as e:
            app.logger.error(f"Database initialization error: {str(e)}")
            db.session.rollback()  # Rollback on error
            # Try to create tables if they don't exist
            db.create_all()
            app.logger.info("Database tables created")

    # Register blueprints
    from backend.appointments.routes import appt_bp
    from backend.auth.routes import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(appt_bp, url_prefix="/appointments")

    return app
