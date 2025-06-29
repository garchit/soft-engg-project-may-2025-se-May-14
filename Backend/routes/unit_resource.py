from flask import Flask, request
from flask_restful import Resource
from models.unit import Unit as Course
from flask_login import login_required
from models import db
from sqlalchemy.exc import SQLAlchemyError
from models.lecture import Lecture
from .helper_functions import create_json




class CourseResource(Resource):
    def get(self):
        courses = Course.query.all()
        course_data=[]
        for course in courses:
            course_data.append(create_json(course))
            
        if not Course:
            return {"error":"Course not found"},404
        print(course_data)
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
    
        Course=db.session.query(Course).filter(Course.id==id).first()
        if not Course:
            return {"error":"Course not found"},404
        try:
            Course.title =title
            Course.description=description
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
            Course=db.session.query(Course).filter(Course.id==id).first()
            if not Course:
                return {"error":"No such Course"}
            db.session.delete(Course)
            db.session.commit()
            return {"message":"Course Deleted Successfully"},200
        except:
            return {"error":"Internal Server Error"},500  