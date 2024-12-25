import factory
from factory.faker import Faker
from backend.auth.models import User
from backend.auth.constants import UserRole
from backend.extensions.extensions import db


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user_{n}@example.com")
    phone_number = Faker('numerify', text='###-###-####')
    role = UserRole.STUDENT
    password = 'password123'  # Add default password as a class attribute

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override _create to handle password setting before commit"""
        # Make sure password is included in kwargs
        if 'password' not in kwargs:
            kwargs['password'] = cls.password
            
        # Create instance with password
        obj = super()._create(model_class, *args, **kwargs)
        return obj