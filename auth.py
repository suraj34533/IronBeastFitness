# This file is deprecated and no longer used
# We've moved authentication to use SQLAlchemy directly
# Keeping this file for reference only

import uuid
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager


class User(UserMixin):
    """User class for MongoDB authentication"""

    def __init__(self, username, email, password_hash, _id=None, created_at=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self._id = _id if _id else str(uuid.uuid4())
        self.created_at = created_at if created_at else datetime.utcnow()

    def get_id(self):
        return str(self._id)

    @classmethod
    def get_by_username(cls, username):
        user_data = mongo.db.users.find_one({"username": username})
        return cls.create_from_db_data(user_data) if user_data else None

    @classmethod
    def get_by_email(cls, email):
        user_data = mongo.db.users.find_one({"email": email})
        return cls.create_from_db_data(user_data) if user_data else None

    @classmethod
    def get_by_id(cls, user_id):
        try:
            user_data = mongo.db.users.find_one({"_id": user_id})
            return cls.create_from_db_data(user_data) if user_data else None
        except:
            return None

    @staticmethod
    def create_from_db_data(user_data):
        if not user_data:
            return None
        return User(
            username=user_data.get('username'),
            email=user_data.get('email'),
            password_hash=user_data.get('password_hash'),
            _id=user_data.get('_id'),
            created_at=user_data.get('created_at')
        )

    def save(self):
        """Save user to database"""
        user_data = {
            "_id": self._id,
            "username": self.username,
            "email": self.email.lower(),
            "password_hash": self.password_hash,
            "created_at": self.created_at
        }
        mongo.db.users.insert_one(user_data)
        return self

    @staticmethod
    def register(username, email, password):
        """Register a new user"""
        # Check if username or email already exists
        if User.get_by_username(username) or User.get_by_email(email):
            return None

        # Create new user
        password_hash = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=password_hash)
        user.save()
        return user

    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader function"""
    return User.get_by_id(user_id)