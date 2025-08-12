
from datetime import date
from extension import db
from models.user import User # This import is now used directly below

class StreakLog(db.Model):
    __tablename__ = 'streak_logs'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    checkin_date = db.Column(db.Date, default=date.today, primary_key=True, nullable=False)

    # ✅ THE FIX: Remove the quotes around 'User' to pass the actual class
    user = db.relationship(User, backref='streak_logs')