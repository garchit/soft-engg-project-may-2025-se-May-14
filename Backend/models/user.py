from models import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
# from flask_login import     current_user,login_manager
from flask_restful import Resource, request
from extension import login_manager

class User(db.Model,UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Use hashed passwords in real apps
    email = db.Column(db.String(120), unique=True, nullable=False)
    parents_email = db.Column(db.String(120), nullable=True)
    dob = db.Column(db.Date, nullable=False)
    rewards = db.Column(db.Integer, default=0)
    picture = db.Column(db.String(255),default='/static/user_placeholder.png')
    user_type = db.Column(db.Boolean, nullable=False)
    # institute_id = db.Column(db.Integer, nullable=False)
    institute_id = db.Column(db.Integer, db.ForeignKey('institute.id', ondelete='CASCADE'), nullable=False)
    streak = db.Column(db.Integer, default=0)
    streak_start_timestamp = db.Column(db.DateTime, nullable=True)
    latest_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_class = db.Column(db.String(50), nullable=True)
    verified = db.Column(db.Integer, default=0)

    institute = relationship("Institute", back_populates="users")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    