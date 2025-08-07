from flask_restful import Resource
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from models.unit import Unit as Course
from models.user_course import UserCourse
from .recommended_courses import recommend_courses_semantic
from models import db

# Optional: Caching the course catalog if needed
from functools import lru_cache

@lru_cache(maxsize=1)
def get_all_courses():
    try:
        courses = db.session.query(Course).all()
        return {course.title: course.description for course in courses}
    except SQLAlchemyError as e:
        print(f"Database error fetching all courses: {str(e)}")
        return {}

class RecommendedCourses(Resource):
    def get(self, user_id):
        try:
            all_courses = get_all_courses()
            if not all_courses:
                return {"error": "No course data available."}, 500

            completed_courses = (
                db.session.query(Course.title)
                .join(UserCourse, UserCourse.course_id == Course.id)
                .filter(UserCourse.user_id == user_id)
                .all()
            )
            completed_titles = [c.title for c in completed_courses]

            recommended = recommend_courses_semantic(completed_titles, all_courses)

            return {"Recommended_Courses": recommended}

        except SQLAlchemyError as db_err:
            print(f"Database error: {str(db_err)}")
            return {"error": "A database error occurred."}, 500

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return {"error": "An unexpected error occurred."}, 500
