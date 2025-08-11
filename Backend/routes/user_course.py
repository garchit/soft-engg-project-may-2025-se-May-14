from flask import request
from flask_restful import Resource
from models import db
from models.user_course import UserCourse
from models.user import User
from models.unit import Unit
from sqlalchemy.exc import SQLAlchemyError


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
        """
        Add or update the marks scored for a user's course.

        Highest score only:
        - If a record exists, update only if the new score is higher.
        - If no record exists, create a new one.
        """
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            course_id = data.get('course_id')
            marks_scored = data.get('marks_scored')

            # Validate required fields
            if user_id is None or course_id is None or marks_scored is None:
                return {
                    "message": "Missing required data: 'user_id', 'course_id', and 'marks_scored' are all required."
                }, 400

            # Ensure marks_scored is numeric
            try:
                marks_scored = float(marks_scored)
            except ValueError:
                return {"message": "'marks_scored' must be a number."}, 400

            # Check for existing record
            user_course = UserCourse.query.filter_by(
                user_id=user_id,
                course_id=course_id
            ).first()

            if user_course:
                # Update only if higher
                if marks_scored > user_course.marks_scored:
                    user_course.marks_scored = marks_scored
                    db.session.commit()
                    return {
                        "message": "User course marks updated to the new highest score."
                    }, 200
                else:
                    return {
                        "message": "The provided score is not higher than the existing score. No update performed."
                    }, 200
            else:
                # Create new record
                new_user_course = UserCourse(
                    user_id=user_id,
                    course_id=course_id,
                    marks_scored=marks_scored
                )
                db.session.add(new_user_course)
                db.session.commit()
                return {"message": "User course record created successfully."}, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": "Database error occurred during POST operation.",
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
