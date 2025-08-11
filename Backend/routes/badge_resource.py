from models import db
from models.badges import badge_user, Badge
from models.user import User
from models.streaklog import StreakLog
from models.user_lecture import UserLecture
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from models import db


# ------------------ Helper Functions ------------------

def get_completed_lectures_count(user_id):
    """Return the total number of completed lectures for a given user."""
    return db.session.query(UserLecture).filter_by(user_id=user_id).count()


def award_if_not_awarded(badge_name, awarded_badge_ids, new_badges, user):
    """Award a badge to the user if they don't already have it, and add badge points to user rewards."""
    badge = Badge.query.filter_by(name=badge_name).first()
    if badge and badge.id not in awarded_badge_ids:
        # Insert new badge for user
        db.session.execute(
            badge_user.insert().values(user_id=user.id, badge_id=badge.id)
        )
        # Add badge to newly awarded list
        new_badges.append(badge)
        
        # Add badge's reward points to user's rewards
        # Assumes badge has a 'points' attribute representing reward points for this badge
        points_to_add = getattr(badge, 'points', 0)  
        if points_to_add:
            user.rewards = (user.rewards or 0) + points_to_add


def get_user_rank(user_id):
    """Calculates the user's rank based on rewards (highest first)."""
    users = User.query.order_by(User.rewards.desc()).all()
    for idx, u in enumerate(users, start=1):
        if u.id == user_id:
            return idx
    return None


def check_and_award_badges(user_id):
    """Check all badge conditions and award new ones if earned."""
    user = User.query.get(user_id)
    if not user:
        return []

    # Ensure user.badges relationship exists in User model
    awarded_badge_ids = set(
        db.session.query(badge_user.c.badge_id).filter(badge_user.c.user_id == user_id).all()
    )
    awarded_badge_ids = {bid for (bid,) in awarded_badge_ids}
    new_badges = []

    # ---------- 1. Streak Badges ----------
    streak_days = db.session.query(StreakLog).filter_by(user_id=user.id).count()
    if streak_days >= 1:
        award_if_not_awarded("First Login", awarded_badge_ids, new_badges, user)
    if streak_days >= 7:
        award_if_not_awarded("Week Warrior", awarded_badge_ids, new_badges, user)
    if streak_days >= 30:
        award_if_not_awarded("Month Master", awarded_badge_ids, new_badges, user)

    # ---------- 2. Rank Badges ----------
    rank = get_user_rank(user.id)
    if rank is not None:
        if rank <= 50:
            award_if_not_awarded("Rising Star", awarded_badge_ids, new_badges, user)
        if rank <= 10:
            award_if_not_awarded("Pro Player", awarded_badge_ids, new_badges, user)

        if user.rewards > 0:
            if rank == 3:
                award_if_not_awarded("Bronze Champion", awarded_badge_ids, new_badges, user)
            if rank == 2:
                award_if_not_awarded("Silver Champion", awarded_badge_ids, new_badges, user)
            if rank == 1:
                award_if_not_awarded("Gold Champion", awarded_badge_ids, new_badges, user)

    # ---------- 3. Rewards Milestones ----------
    if user.rewards >= 100:
        award_if_not_awarded("Centurion", awarded_badge_ids, new_badges, user)
    if user.rewards >= 500:
        award_if_not_awarded("Halfway Hero", awarded_badge_ids, new_badges, user)
    if user.rewards >= 1000:
        award_if_not_awarded("Reward Legend", awarded_badge_ids, new_badges, user)

    # ---------- 4. Lecture Completion ----------
    lectures_completed = get_completed_lectures_count(user.id)
    if lectures_completed >= 1:
        award_if_not_awarded("Quick Learner", awarded_badge_ids, new_badges, user)
    if lectures_completed >= 5:
        award_if_not_awarded("Consistent Learner", awarded_badge_ids, new_badges, user)
    if lectures_completed >= 10:
        award_if_not_awarded("Knowledge Collector", awarded_badge_ids, new_badges, user)

    if new_badges:
        db.session.commit()

    return new_badges


# ------------------ Resource Class ------------------

class BadgeResource(Resource):
    def get(self, id=None):
        try:
            if id is None:
                badges = db.session.query(Badge).all()
                return {
                    "list_badges": [
                        {"id": b.id, "name": b.name, "description": b.description, "points": b.points}
                        for b in badges
                    ]
                }, 200

            badge = db.session.query(Badge).filter_by(id=id).first()
            if not badge:
                return {"message": f"Badge with id {id} not found."}, 404

            return {
                "id": badge.id,
                "name": badge.name,
                "description": badge.description,
                "points": badge.points
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error.", "details": str(e)}, 500

    def put(self,id):
        if id==None:
            return {"message": "Badge ID is required for update."}, 400

        try:
            data = request.get_json(force=True)
            if not data:
                return {"message": "Request body is missing or invalid JSON."}, 400

            name = data.get("name")
            description = data.get("description")
            points = data.get("points")

            if name is None or description is None or points is None:
                return {"message": "Fields 'name', 'description', and 'points' are required."}, 400
            if not isinstance(points, int) or points < 0:
                return {"message": "'points' must be a non-negative integer."}, 400

            badge = db.session.query(Badge).filter(Badge.id == id).first()
            if not badge:
                return {"message": f"Badge with id {id} not found."}, 404

            badge.name = name
            badge.description = description
            badge.points = points
            db.session.commit()

            return {
                "message": f"Badge {id} successfully updated.",
                "badge": {
                    "id": badge.id,
                    "name": badge.name,
                    "description": badge.description,
                    "points": badge.points
                }
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error occurred.", "error": str(e)}, 500
        except Exception as e:
            return {"message": "Unexpected error occurred.", "error": str(e)}, 500

    def post(self):
        try:
            data = request.get_json(force=True)
        except Exception:
            return {"error": "Invalid JSON payload."}, 400

        name = data.get('name')
        description = data.get('description')
        points = data.get('points')

        if not name:
            return {"error": "'name' field is required."}, 400
        if points is None:
            return {"error": "'points' field is required."}, 400
        if not isinstance(points, int):
            return {"error": "'points' must be an integer."}, 400
        if Badge.query.filter_by(name=name).first():
            return {"error": f"Badge with name '{name}' already exists."}, 400

        try:
            badge = Badge(name=name, points=points, description=description)
            db.session.add(badge)
            db.session.commit()

            return {
                "message": "Badge created successfully.",
                "badge": {
                    "id": badge.id,
                    "name": badge.name,
                    "points": badge.points,
                    "description": description
                }
            }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error.", "details": str(e)}, 500
        except Exception as e:
            return {"error": "Unexpected error occurred.", "details": str(e)}, 500

    def delete(self, id):
        try:
            badge = db.session.query(Badge).filter(Badge.id == id).first()
            if not badge:
                return {"message": f"Badge with id {id} not found."}, 404

            db.session.delete(badge)
            db.session.commit()

            return {"message": f"Badge {id} successfully deleted."}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error occurred.", "error": str(e)}, 500
        except Exception as e:
            return {"message": "Unexpected error occurred.", "error": str(e)}, 500

class UserBadgesApi(Resource):
    def get(self, user_id):
        try:
            user = db.session.query(User).get(user_id)
            if not user:
                return {"error": f"User with ID {user_id} not found"}, 404

            # Manual query joining badge_user and Badge to get badges of user
            badges = (
                db.session.query(Badge)
                .join(badge_user, Badge.id == badge_user.c.badge_id)
                .filter(badge_user.c.user_id == user_id)
                .all()
            )

            awarded_badges = [
                {
                    "id": badge.id,
                    "name": badge.name,
                    "description": badge.description,
                    "points": badge.points
                }
                for badge in badges
            ]

            return {"user_id": user_id, "badges": awarded_badges}, 200

        except Exception as e:
            return {
                "message": "An unexpected error occurred during GET operation.",
                "error": str(e)
            }, 500
