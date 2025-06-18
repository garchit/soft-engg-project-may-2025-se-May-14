from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from werkzeug.exceptions import HTTPException
import json
from datetime import date,timedelta
from flask_jwt_extended import create_access_token,jwt_required
from time import perf_counter_ns
from models import db
from models.institute import Institute
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user

class InstituteResource(Resource):
       # @login_required
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

              
              
              
       def put(self,id):
              pass          


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

       def delete(self,id):
              print("Inside delte of USer Api")