from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from models.unit import Unit as Course
from models.user_course import UserCourse
from .recommended_courses import recommend_courses_semantic 
from extension import db
from flask_login import login_required, current_user

# Using a cached function for all courses is a good optimization
from functools import lru_cache

@lru_cache(maxsize=1)
def get_all_courses_dict():
    try:
        courses = db.session.query(Course).all()
        return {course.title: course.description for course in courses}
    except SQLAlchemyError as e:
        print(f"Database error fetching all courses: {str(e)}")
        return {}

class RecommendedCourses(Resource):
    @login_required
    def get(self, user_id):
        # Security check to ensure users can only see their own recommendations
        if current_user.id != user_id:
            return {"error": "Unauthorized access"}, 403
            
        try:
            # Step 1: Get all courses for the recommender
            all_courses = get_all_courses_dict()
            if not all_courses:
                return {"error": "No course data available."}, 500

            # Step 2: Get titles of courses the user has completed
            completed_courses = (
                db.session.query(Course.title)
                .join(UserCourse, UserCourse.course_id == Course.id)
                .filter(UserCourse.user_id == user_id)
                .all()
            )
            completed_titles = [c.title for c in completed_courses]

            # Step 3: Get a list of recommended course titles from your AI function
            recommended_titles = recommend_courses_semantic(completed_titles, all_courses, top_n=4)

            # ✅ THE FIX: Fetch full details for the recommended titles
            recommended_course_details = []
            if recommended_titles:
                # Query the database for the course objects that match the recommended titles
                recommended_courses_query = Course.query.filter(Course.title.in_(recommended_titles)).all()
                
                # Create a list of dictionaries with the data the frontend needs
                recommended_course_details = [
                    {
                        "id": course.id,
                        "title": course.title,
                        # NOTE: You may want to add an image_url column to your Unit model
                        "image_url": "/src/assets/default-course.jpg" 
                    }
                    for course in recommended_courses_query
                ]
            
            # ✅ CHANGED: Return the list of course objects
            return {"recommendations": recommended_course_details}, 200

        except Exception as e:
            print(f"Unexpected error in recommendations: {str(e)}")
            return {"error": "An unexpected error occurred."}, 500