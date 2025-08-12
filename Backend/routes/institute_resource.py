from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import  Resource
import json
from extension import db
from models.institute import Institute
from models.user import User
from flask_login import login_required
from .helper_functions import to_dict,count_students,average_institute_score
from sqlalchemy.exc import SQLAlchemyError
from models.teacher import Teacher

class InstituteResource(Resource):
       @login_required
       def get(self,id):
              institute=db.session.query(Institute).filter(Institute.id==id).first()
              try:
                     if institute==None:
                            return {"error":"No such User"},404
                     elif institute:
                            return {"message":"Found Institute",
                                    "Name":institute.name,
                                    "Address":institute.address,
                                    "email":institute.email,
                                    "password":institute.password
                                    }
              except:
                     return {"error":"Interval Server Error"},500

       @login_required       
       def put(self,id):
              data=request.get_json()
              name=data.get("name")
              address=data.get("address")
              institute=db.session.query(Institute).filter(Institute.id==id).first()
              if institute==None:
                     return {"error":"No such Institute"},404
              if name=="" or name==None:
                     return {"error":"bad Request"},400
              if institute:
                     try:

                            institute.name=name
                            institute.address=address
                            db.session.commit()
                            return {"message":"Successfully Updated"},200
                     except:
                            return {"error":"Internal Server Error"},500
      
       def post(self):
              data = request.get_json(force=True)  # or without force if header is set correctl
              new_institute = Institute(
                     name=data.get("name"),
                     email=data.get("email"),
                     password=data.get("password"), 
                     address=data.get("address"),
                     blocked=0
                     )
              check_by_name=db.session.query(Institute).filter(Institute.name == new_institute.name).first()
              check_by_email=db.session.query(Institute).filter(Institute.email == new_institute.email).first()
              try:
                if check_by_name:
                        return {"error":"Institue is already exist"},401
                elif check_by_email:
                        return {"error":"Email is already in use"},401
                elif new_institute.name is None or new_institute.name=="":
                        return {"error":"Institue name cannot be empty"},401
                elif new_institute.address is None or new_institute.address=="":
                        return {"error":"address name cannot be empty"},401
                elif new_institute.email is None or new_institute.email=="":
                        return {"error":"Email cannot be empty"},401
              
                db.session.add(new_institute)
                db.session.commit()
              except:
                     return {"error":"Internal Server Error"},500

              return {"message": "User created successfully"   }, 201
      
       @login_required
       def delete(self,id):
              try:
                     institute=db.session.query(Institute).filter(Institute.id==id).first()
                     if institute is None:
                            return {"error":"No such Institute"},404
                     db.session.delete(institute)
                     db.session.commit()
                     return {"message":"Deleted Succesfully"},200
              except:
                     return {"error":"Internal Server Error"},500
              


class AllInstitute(Resource):
       def get(self):
              all_institues=Institute.query.all()
              json_list=[]
              for each_institute in all_institues:
                     total_students=count_students(each_institute.id)
                     if each_institute.id!=-1:
                            json_list.append(to_dict(each_institute,total_students))
                     else:
                            json_list.append({"id":-1,
                                              "name":"Independent Students",
                                              "email":"Not Applicable",
                                              "total_students":total_students,
                                              "blocked":"You cannot block me!!"
                                              })

              return json_list,200

class ToggleBlockInstitute(Resource):
       def put(self,institute_id):
              try:

                     institute=db.session.query(Institute).filter(Institute.id==institute_id).first()
                     if not institute:
                            return {"error":"No such institute"},404
                     blocked=institute.blocked
                     if blocked==0:
                            institute.blocked=1
                     else:
                            institute.blocked=0
                     db.session.commit()
                     return {"message":"Action done successfully"},200
              except SQLAlchemyError as e:
                     db.session.rollback()
                     return {"error": "Internal Server Error", "details": str(e)}, 500
              
class InstituteTeacher(Resource):
    def get(self, institute_id):
        try:
            #Check if the institute exists
            institute = db.session.query(Institute).filter_by(id=institute_id).first()
            if not institute:
                return {
                    "message": f"Institution with id {institute_id} not found.",
                    "teachers": []
                }, 404

            #Fetch teachers in this institute
            teachers = db.session.query(Teacher).filter_by(institute_id=institute_id).all()

            # Serialize teachers
            teacher_list = [
                {
                    "id": teacher.id,
                    "name": teacher.name,
                    "email": teacher.email,
                    "class": teacher.class_teacher
                }
                for teacher in teachers
            ]

            return {
                "message": "Successfully fetched teachers.",
                "teachers": teacher_list
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": "Database error occurred.",
                "error": str(e)
            }, 500

        except Exception as e:
            return {
                "message": "Unexpected error occurred.",
                "error": str(e)
            }, 500
              
class InstituteInfo(Resource):
    def get(self, institute_id):
       try:
              institute = db.session.query(Institute).filter_by(id=institute_id).first()
              if not institute:
                     return {"error": "Institute not found"}, 404
              
              # Fetching the number of students
              total_students = count_students(institute_id)
              total_teachers = db.session.query(Teacher).filter(Teacher.institute_id == institute_id).count()
              average_score=average_institute_score(institute_id)
              return {
                     "id": institute.id,
                     "name": institute.name,
                     "email": institute.email,
                     "address": institute.address,
                     "total_students": total_students,
                     "total_teachers": total_teachers,
                     "blocked": institute.blocked,
                     "average_institute_score": average_score
              }, 200

       except SQLAlchemyError as e:
              db.session.rollback()
              return {"error": "Internal Server Error", "details": str(e)}, 500



