from flask import request
from flask_restful import Resource
from extension import db
from models.user_course import UserCourse
from models.user import User
from models.unit import Unit
from sqlalchemy.exc import SQLAlchemyError
# from .badge_resource import check_and_award_badges


class UserCoursesApi(Resource):
    def get(self):
        """
        Fetch all user-course records with user details and course details.
        """
        try:
            user_courses = (
                db.session.query(UserCourse, User, Unit)
                .outerjoin(User, UserCourse.user_id == User.id)
                .outerjoin(Unit, UserCourse.course_id == Unit.id)
                .all()
            )

            if not user_courses:
                return {"message": "No user-course records found."}, 404

            data = [
                {
                    "user_id": uc.UserCourse.user_id,
                    "username": uc.User.username if uc.User else None,
                    "course_id": uc.UserCourse.course_id,
                    "course_title": uc.Unit.title if uc.Unit else None,
                    "marks_scored": uc.UserCourse.marks_scored,
                }
                for uc in user_courses
            ]

            return {
                "message": "Successfully fetched all user-course records.",
                "user_courses": data
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error occurred.", "error": str(e)}, 500

        except Exception as e:
            return {"message": "An unexpected error occurred.", "error": str(e)}, 500
        
    def post(self):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            course_id = data.get('course_id')
            marks_scored = data.get('marks_scored')

            if not all([user_id, course_id, marks_scored is not None]):
                return {"message": "Missing required data: user_id, course_id, or marks_scored."}, 400
            
            if not isinstance(marks_scored, (int, float)):
                return {"message": "Invalid data type for marks_scored. Must be a number."}, 400

            user_course = UserCourse.query.filter_by(user_id=user_id, course_id=course_id).first()
            user = User.query.get(user_id)
            if not user:
                return {"message": f"User with ID {user_id} not found."}, 404

            rewards_to_add = 0
            message = ""

            if user_course:
                if marks_scored > user_course.marks_scored:
                    rewards_to_add = marks_scored - user_course.marks_scored
                    user_course.marks_scored = marks_scored
                    user.rewards = (user.rewards or 0) + rewards_to_add
                    message = f"User course marks updated to the new highest score. User awarded {rewards_to_add} rewards."
                else:
                    message = "The provided score is not higher than the existing score. No update performed."
            else:
                rewards_to_add = marks_scored
                new_user_course = UserCourse(user_id=user_id, course_id=course_id, marks_scored=marks_scored)
                db.session.add(new_user_course)
                user.rewards = (user.rewards or 0) + rewards_to_add
                message = f"User course record created successfully. User awarded {rewards_to_add} rewards."

            db.session.commit()

            # Badge awarding can update DB, so safe to call after commit or inside with session
            # newly_awarded_badges = check_and_award_badges(user.id)

            response_data = {"message": message, "current_rewards": user.rewards}
            # if newly_awarded_badges:
                # response_data["new_badges"] = [{"name": b.name, "description": b.description} for b in newly_awarded_badges]

            return response_data, 200 if user_course else 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": "Database error occurred during POST operation. Please try again.",
                "error": str(e)
            }, 500
        except Exception as e:
            return {
                "message": "An unexpected error occurred during POST operation.",
                "error": str(e)
            }, 500


class UserCoursesByUserApi(Resource):
    def get(self, user_id):
        """
        Fetch all courses for a specific user by user_id.
        """
        try:
            user_courses = (
                db.session.query(UserCourse, Unit)
                .join(Unit, UserCourse.course_id == Unit.id)
                .filter(UserCourse.user_id == user_id)
                .all()
            )

            if not user_courses:
                return {"message": f"No courses found for user ID {user_id}."}, 404

            data = [
                {
                    "course_id": uc.Unit.id,
                    "course_title": uc.Unit.title,
                    "marks_scored": uc.UserCourse.marks_scored,
                }
                for uc in user_courses
            ]

            return {
                "message": f"Successfully fetched courses for user ID {user_id}.",
                "courses": data
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error occurred.", "error": str(e)}, 500

        except Exception as e:
            return {"message": "An unexpected error occurred.", "error": str(e)}, 500
