from flask import Flask, request
from flask_restful import Resource
from models.unit import Unit as Course
from flask_login import login_required, current_user # ✅ ADDED: Imports for authentication
from models.user_course import UserCourse
from extension import db
from sqlalchemy.exc import SQLAlchemyError
from models.lecture import Lecture
from .helper_functions import create_json, course_progress
from models.user import User

# ✅ ADDED: Helper function to convert a score to a grade
def calculate_grade(score):
    if not isinstance(score, (int, float)):
        return "N/A"
    if score >= 95: return "S"
    if score >= 85: return "A"
    if score >= 75: return "B"
    if score >= 65: return "C"
    return "D"

class CourseResource(Resource):
    def get(self,id=None):
        if id:
            course=db.session.query(Course).filter(Course.id==id).first()
            if not course:
                return {"error":"Course Not Found"},404
            course_data=create_json(course=course)
            return {"message":"Course Fetched Successfully",
                    "course_details":course_data
                    },200
        courses = Course.query.all()
        course_data=[]
        for course in courses:
            course_data.append(create_json(course))
            
        if not courses: # Corrected this line
            return {"error":"Course not found"},404
        return{
            "message":"Course Found",
            "course_detail":course_data
        },200
    
    def post(self):
        # ... your existing post logic ...
        data=request.get_json(force=True)
        title=data.get("title")
        description=data.get("description")     
        try:
            check_by_title=db.session.query(Course).filter(Course.title==title).first()
            if check_by_title:
                return {"error":"Title Already Exist"},400
            new_Course=Course(title=title,description=description)
            db.session.add(new_Course)
            db.session.commit()
            return {"message":"Course added Succesfully"},201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Internal Server Error", "details": str(e)}, 500
    
    def put(self,id):
        # ... your existing put logic ...
        data=request.get_json(force=True)
        title=data.get("title")
        description=data.get("description")
        check_title=db.session.query(Course).filter(Course.id!=id,Course.title==title).first()
        if check_title:
            return {"error":"Title already Exist"},400
    
        course=db.session.query(Course).filter(Course.id==id).first()
        if not course: # Corrected this line
            return {"error":"Course not found"},404
        try:
            course.title =title
            course.description=description
            db.session.commit()
            return {
                "message":"Course Updated Succesfully",
                "title":title,
                "description":description
            },200
        except:
            return {"error":"Internal Server Error"},500
    
    def delete(self,id):
        # ... your existing delete logic ...
        try:
            course=db.session.query(Course).filter(Course.id==id).first()
            if not course:
                return {"error":"No such Course"}
            db.session.delete(course)
            db.session.commit()
            return {"message":"Course Deleted Successfully"},200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error":"Internal Server Error","details":str(e)},500  
        
class CompletedCourse(Resource):
    @login_required # ✅ ADDED: Protect the route
    def get(self, user_id):
        # ✅ IMPLEMENTED: The logic to fetch completed courses
        if current_user.id != user_id:
            return {"error": "Unauthorized"}, 403

        try:
            completed = db.session.query(
                Course.id,
                Course.title,
                UserCourse.marks_scored
            ).join(UserCourse, UserCourse.course_id == Course.id).filter(
                UserCourse.user_id == user_id
            ).all()

            completed_courses_data = [
                {
                    "id": c.id,
                    "title": c.title,
                    "grade": calculate_grade(c.marks_scored),
                    "image_url": "/src/assets/demand&supply.jpg" # Placeholder image
                }
                for c in completed
            ]
            return {"completed_courses": completed_courses_data}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error", "details": str(e)}, 500

    def post(self,user_id):
        # ... your existing post logic remains unchanged ...
        data=request.get_json(force=True)
        course_id=data.get("course_id")
        marks_scored=data.get("marks_scored")
        user=User.query.get(user_id)
        if not user:
            return {"error":"No such User"},404
        course=db.session.query(Course).filter(Course.id==course_id).first()
        if not course:
            return {"error":"No such course exist"},404
        try:
            user_course_completed=UserCourse(user_id=user_id,course_id=course_id,marks_scored=marks_scored)
            db.session.add(user_course_completed)
            db.session.commit()
            return {"message":"Successfully Added"},201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error":"Internal Server Error","details":str(e)},500

class CourseProgress(Resource):
    # ... your existing CourseProgress resource remains unchanged ...
    def get(self,user_id):
        course_total_progress=course_progress(user_id)
        sum_progress=0
        for progress in course_total_progress:
            sum_progress+=list(progress.values())[0]
        total_courses=db.session.query(Course).count()
        if total_courses == 0: # Avoid division by zero
            return {"course_progress": [], "overall_progress": 0}, 200
        overall_progress=sum_progress/total_courses
        return {"course_progress":course_total_progress,"overall_progress":round(overall_progress,2)},200