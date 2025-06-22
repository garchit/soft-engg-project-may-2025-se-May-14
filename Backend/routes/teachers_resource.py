from flask import Flask, request
from flask_restful import Resource
import json
from models.teacher import Teacher
from models.institute import Institute
from flask_login import login_required
from models import db

class TeacherResource(Resource):
    @login_required
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

        
    @login_required
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

    @login_required
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