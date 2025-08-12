from flask import Flask, request
from flask_restful import Resource
import json
from models.teacher import Teacher
from models.institute import Institute
from flask_login import login_required
from extension import db
from models.user_teacher import UserTeacher
from models.user import User
from .helper_functions import getTeachers,overall_progress, getTeacherName
from sqlalchemy.exc import SQLAlchemyError

class TeacherResource(Resource):
    # @login_required
    def get(self,id):
        try:
            teacher = db.session.query(Teacher).filter(Teacher.id==id).first()
            if not teacher:
                return {"Error":"Bad Request"},401

            return {
                    "message":"Teacher Found",
                    "name":teacher.name,
                    "institute_id":teacher.institute_id,
                    "email":teacher.email,
                    "class_teacher":teacher.class_teacher
                },200
        except:
            return {"error":"Internal Server Error"},500

        
    # @login_required
    def put(self,id):
        data=request.get_json(force=True)
        name=data.get("name")
        password=data.get("password")
        class_teacher=data.get("class_teacher")
        
        if name is None or password is None  or class_teacher is None:
            return {"error":"Required Field is Missing"},401
        if name =="" or password ==""  or class_teacher == "":
            return {"error":"Required Field is Missing"},401
        
    
        if class_teacher<1 or class_teacher>12:
            return {"error":"Invalind Class"},400
        
        try:
        
            teacher=db.session.query(Teacher).filter(Teacher.id==id).first()
            if teacher:
                teacher.name=name
                teacher.password=password
                teacher.class_teacher=class_teacher
                db.session.commit()
            
                return {"message":"Teacher Updated Successfully"},200
            else:
                return {"error":"Teacher not found"},404
        
        except:
            return {"error":"Internal Sever Error"},500

    # @login_required
    def post(self):
        data=request.get_json(force=True)
        name=data.get("name")
        password=data.get("password")
        institute_id=data.get("institute_id")
        email=data.get("email")
        class_teacher=data.get("class_teacher") 
        if name is None or password is None  or email is None  or class_teacher is None or institute_id==None:
            return {"error":"Required Field is Missing"},401
        if name =="" or password ==""  or email ==""  or class_teacher == "" or institute_id=="":
            return {"error":"Required Field is Missing"},401
        
        institute = db.session.get(Institute, institute_id)
        if not institute:
            return {"error":"No such institue, Bad Request"},401
        teacher=db.session.query(Teacher).filter(Teacher.email==email).first()
        if teacher:
            return {"error":"Email already in Use"},400
        if class_teacher<1 or class_teacher>12:
            return {"error":"Invalind Class"},400
        
        try:
            check_class_exist=db.session.query(Teacher).filter(Teacher.class_teacher==class_teacher,Teacher.institute_id==institute_id).first()
            if check_class_exist:
                return {"error":"This class already has a class teacher"},401
            
            teacher_data=Teacher(name=name,password=password,institute_id=institute_id,email=email,class_teacher=class_teacher)
            db.session.add(teacher_data)
            db.session.commit()
            
            return {"message":"Teacher Added Successfully"},201
        except:
            return {"error":"Internal Sever Error"},500

        
    @login_required
    def delete(self,id):
        try:
            teacher=db.session.query(Teacher).filter(Teacher.id==id).first()
            if not teacher:
                return {"error":"There is no such teacher"},401

            db.session.delete(teacher)
            db.session.commit()
            return {"message":"Teacher is Successfully Removed from Institue"},200
        except:
            return {"error":"OOps there is Internal Server Occur"},500
    
class UserTeacherResource(Resource):
    def get():
        pass
    def post(self, user_id):
        try:
            check_user = db.session.query(User).filter(User.id == user_id).first()
            if not check_user:
                return {"error": "No such user"}, 404

            existing_link = db.session.query(UserTeacher).filter(UserTeacher.user_id == user_id).first()
            if existing_link:
                return {"error": "User is already assigned to a teacher"}, 401
            check_class=check_user.user_class
            teacher=db.session.query(Teacher).filter(Teacher.class_teacher==check_class,Teacher.institute_id==check_user.institute_id).first()
            if not teacher:
                return {"error":"There is no teacher assigned to this class"},401
    

            user_teacher = UserTeacher(user_id=user_id,teacher_id=teacher.id)
            db.session.add(user_teacher)
            db.session.commit()

            return {"message": "Linked student to teacher"}, 200

        except Exception as e:
            db.session.rollback()
            return {"error": "An unexpected error occurred", "details": str(e)}, 500
        
class TeacherWiseProgress(Resource):
    def get(self,institute_id):
        teachers=getTeachers(institute_id=institute_id)
        teacher_wise=[]
        try:
            for teacher_id in teachers:
                all_progress=[]
                students=db.session.query(UserTeacher).filter(UserTeacher.teacher_id==teacher_id)
                name = getTeacherName(teacher_id)
                total=0
                for student in students:
                    user_id=student.user_id
                    student_details=db.session.query(User).filter(User.id==user_id).first()
                    progress=overall_progress(user_id=user_id)
                    total+=progress
                    print(student_details.dob)
                    all_progress.append({"student_name":student_details.full_name,
                                        "dob":str(student_details.dob),
                                        "student_id":student_details.id,
                                        "student_name":student_details.full_name,
                                        "overall_progress":progress})
                average=total/students.count() if students.count() > 0 else 0
                teacher_wise.append({"teacher_id":teacher_id, "teacher_name": name, "student_details":all_progress,"teacher_progress":round(average,2)})
            return {"teacher_progress":teacher_wise}
        except SQLAlchemyError as e:    
            return {"error":"internal server error","details":str(e)},500
        

          
            


