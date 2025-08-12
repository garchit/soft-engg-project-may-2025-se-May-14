from flask import request
from flask_restful import Resource
from extension import db
from models.user import User
from sqlalchemy.exc import SQLAlchemyError


class LeaderboardApi(Resource):
    def get(self):
        """
        Fetch all students sorted by their rewards (XP) in descending order.
        Adds rank to each student.
        """
        try:
            students = (
                db.session.query(User)
                .filter(User.user_type == 0)  # Only students, not admins
                .order_by(User.rewards.desc())
                .all()
            )

            if not students:
                return {"message": "No students found."}, 404

            leaderboard = [
                {
                    "rank": idx + 1,
                    "id": student.id,
                    "username": student.username,
                    "rewards": student.rewards,
                    "streak": student.streak,
                    "picture": student.picture,
                }
                for idx, student in enumerate(students)
            ]

            return {
                "message": "Successfully fetched leaderboard.",
                "leaderboard": leaderboard
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error occurred.", "error": str(e)}, 500

        except Exception as e:
            return {"message": "An unexpected error occurred.", "error": str(e)}, 500


class UserRankApi(Resource):
    def get(self, username):
        """
        Fetch a specific student's rank, rewards, and progress to next rank.
        """
        try:
            students = (
                db.session.query(User)
                .filter(User.user_type == 0)  # Only students, not admins
                .order_by(User.rewards.desc())
                .all()
            )

            for idx, student in enumerate(students, start=1):
                if student.username.lower() == username.lower():
                    next_rank = students[idx - 2] if idx > 1 else None
                    points_to_next = (next_rank.rewards - student.rewards) if next_rank else 0

                    return {
                        "id": student.id,
                        "username": student.username,
                        "full_name": student.full_name, # ✅ ADD THIS LINE
                        "rewards": student.rewards,
                        "rank": idx,
                        "streak": student.streak,
                        "points_to_next_rank": points_to_next
                    }, 200

            return {"message": f"User '{username}' not found."}, 404

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error occurred.", "error": str(e)}, 500

        except Exception as e:
            return {"message": "An unexpected error occurred.", "error": str(e)}, 500

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error occurred.", "error": str(e)}, 500

        except Exception as e:
            return {"message": "An unexpected error occurred.", "error": str(e)}, 500
