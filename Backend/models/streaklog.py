from models import db
from datetime import date
from models.user import User

class StreakLog(db.Model):
    __tablename__ = 'streak_logs'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    checkin_date = db.Column(db.Date, default=date.today, primary_key=True, nullable=False)

    user = db.relationship('User', backref='streak_logs')