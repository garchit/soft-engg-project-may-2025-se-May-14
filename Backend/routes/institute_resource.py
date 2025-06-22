from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import  Resource
import json
from models import db
from models.institute import Institute
from flask_login import login_required

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
                     address=data.get("address")
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