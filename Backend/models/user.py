# In models/user.py

from extension import db              # ✅ CORRECTED: Imports 'db' from the central extension.py file
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

# Note: login_manager and other imports for routes are not needed in a model file.

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Remember to hash passwords!
    email = db.Column(db.String(120), unique=True, nullable=False)
    parents_email = db.Column(db.String(120), nullable=True)
    dob = db.Column(db.Date, nullable=False)
    rewards = db.Column(db.Integer, default=0)
    picture = db.Column(db.String(255), default='/static/user_placeholder.png')
    user_type = db.Column(db.Boolean, nullable=False)
    institute_id = db.Column(db.Integer, db.ForeignKey('institute.id', ondelete='CASCADE'), nullable=False)
    streak = db.Column(db.Integer, default=0)
    streak_start_timestamp = db.Column(db.DateTime, nullable=True)
    latest_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_class = db.Column(db.String(50), nullable=True)
    verified = db.Column(db.Integer, default=0)

    institute = relationship("Institute", back_populates="users")

# IMPORTANT: Ensure the @login_manager.user_loader decorator and function
# have been DELETED from this file. It belongs ONLY in factory.py.