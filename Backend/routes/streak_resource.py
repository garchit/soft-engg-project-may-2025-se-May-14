from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from extension import db
from flask_restful import Api, Resource
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
from datetime import datetime, timedelta, date
from models.streaklog import StreakLog
from flask import request
from flask_login import login_required, current_user
import pytz
from .badge_resource import check_and_award_badges 


def calculate_longest_streak_up_to_date(user_id, end_date):
    dates = (
        db.session.query(StreakLog.checkin_date)
        .filter(StreakLog.user_id == user_id, StreakLog.checkin_date <= end_date)
        .order_by(StreakLog.checkin_date)
        .all()
    )
    dates = [d[0] for d in dates]

    if not dates:
        return 0

    longest_streak = 1
    current_streak = 1

    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + timedelta(days=1):
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1

    return longest_streak


class StreakResource(Resource):
    # @login_required
    def post(self):
        user = current_user
        today = date.today()
        india_tz = pytz.timezone("Asia/Kolkata")

        # Check if already checked in today
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
                "latest_timestamp": latest_str,
            }, 200

        # Update streak
        yesterday = today - timedelta(days=1)
        last_log = (
            StreakLog.query.filter_by(user_id=user.id)
            .order_by(StreakLog.checkin_date.desc())
            .first()
        )

        if last_log and last_log.checkin_date == yesterday:
            user.streak += 1
        else:
            user.streak = 1
            user.streak_start_timestamp = datetime.utcnow()

        # Save UTC time for latest timestamp
        user.latest_timestamp = datetime.utcnow()

        # Log today's check-in
        db.session.add(StreakLog(user_id=user.id, checkin_date=today))
        db.session.commit()

        longest_streak_before = calculate_longest_streak_up_to_date(user.id, today - timedelta(days=1))
        longest_streak_after = calculate_longest_streak_up_to_date(user.id, today)

        reward_increment = 0
        if longest_streak_after > longest_streak_before:
            diff = longest_streak_after - longest_streak_before
            reward_increment = diff * 10
            user.rewards = (user.rewards or 0) + reward_increment
            db.session.commit()

        newly_awarded_badges = check_and_award_badges(user.id)

        # Format timestamp in IST
        utc_dt = user.latest_timestamp.replace(tzinfo=pytz.utc)
        india_dt = utc_dt.astimezone(india_tz)
        latest_str = india_dt.strftime("%B %d, %Y at %I:%M:%S %p")

        response_data = {
            "message": "Check-in successful!",
            "user_id": user.id,
            "streak": user.streak,
            "longest_streak": longest_streak_after,
            "reward_increment": reward_increment,
            "total_rewards": user.rewards,
            "latest_timestamp": latest_str,
        }

        if newly_awarded_badges:
            response_data["new_badges"] = [
                {"name": b.name, "description": b.description} for b in newly_awarded_badges
            ]

        return response_data, 200

class StreakCalendarData(Resource):
    # @login_required
    def get(self):
        logs = StreakLog.query.filter_by(user_id=current_user.id).all()
        return {
            "checkins": [log.checkin_date.isoformat() for log in logs],
            "streak": current_user.streak
        }

