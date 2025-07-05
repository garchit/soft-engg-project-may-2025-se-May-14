from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db
from flask_restful import Api, Resource
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
from datetime import datetime, timedelta, date
from models.streaklog import StreakLog

from flask import request
from flask_restful import Resource
from flask_login import login_required, current_user
from datetime import date, timedelta, datetime
from models import db
from models.streaklog import StreakLog
import pytz

class StreakResource(Resource):
    @login_required
    def post(self):
        user = current_user
        today = date.today()
        india_tz = pytz.timezone('Asia/Kolkata')

        # Check if already checked in
        if StreakLog.query.filter_by(user_id=user.id, checkin_date=today).first():
            latest_str = None
            if user.latest_timestamp:
                utc_dt = user.latest_timestamp.replace(tzinfo=pytz.utc)
                india_dt = utc_dt.astimezone(india_tz)
                latest_str = india_dt.strftime("%B %d, %Y at %I:%M:%S %p")
            
            return {
                "message": "Already checked in today.",
                "user_id": user.id,
                "streak": user.streak,
                "latest_timestamp": latest_str
            }, 200

        # Handle streak update
        yesterday = today - timedelta(days=1)
        last_log = StreakLog.query.filter_by(user_id=user.id).order_by(StreakLog.checkin_date.desc()).first()

        if last_log and last_log.checkin_date == yesterday:
            user.streak += 1
        else:
            user.streak = 1
            user.streak_start_timestamp = datetime.utcnow()

        # Save UTC time, but return IST
        user.latest_timestamp = datetime.utcnow()

        # Log today's check-in
        db.session.add(StreakLog(user_id=user.id, checkin_date=today))
        db.session.commit()

        # Format timestamp in IST
        utc_dt = user.latest_timestamp.replace(tzinfo=pytz.utc)
        india_dt = utc_dt.astimezone(india_tz)
        latest_str = india_dt.strftime("%B %d, %Y at %I:%M:%S %p")

        return {
            "message": "Check-in successful!",
            "user_id": user.id,
            "streak": user.streak,
            "latest_timestamp": latest_str
        }, 200



class StreakCalendarData(Resource):
    @login_required
    def get(self):
        logs = StreakLog.query.filter_by(user_id=current_user.id).all()
        return {
            "checkins": [log.checkin_date.isoformat() for log in logs],
            "streak": current_user.streak
        }

