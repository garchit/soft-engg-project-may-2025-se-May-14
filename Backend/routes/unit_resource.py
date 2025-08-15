from flask import Flask, request
from flask_restful import Resource
from models.unit import Unit as Course
from flask_login import login_required
from models.user_course import UserCourse
from extension import db
from sqlalchemy.exc import SQLAlchemyError
from models.lecture import Lecture
from .helper_functions import create_json,course_progress
from models.user import User





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
        # print("cc",course_data)
            
        if not Course:
            return {"error":"Course not found"},404
        return{
            "message":"Course Found",
            "course_detail":course_data
        },200
    
    def post(self):
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
        data=request.get_json(force=True)
        title=data.get("title")
        description=data.get("description")
        check_title=db.session.query(Course).filter(Course.id!=id,Course.title==title).first()
        if check_title:
            return {"error":"Title already Exist"},400
    
        course=db.session.query(Course).filter(Course.id==id).first()
        if not Course:
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
    def get(self,user_id):
        pass
    def post(self,user_id):
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
    def get(self,user_id):
        course_total_progress=course_progress(user_id)
        sum_progress=0
        for progress in course_total_progress:
            sum_progress+=list(progress.values())[0]
        total_courses=db.session.query(Course).count()
        overall_progress=sum_progress/total_courses
        return {"course_progress":course_total_progress,"overall_progress":round(overall_progress,2)},200
        