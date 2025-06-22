from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from werkzeug.exceptions import HTTPException
import json
from datetime import date,timedelta
from flask_jwt_extended import create_access_token,jwt_required
from time import perf_counter_ns
from models import db
from models.user import User
from datetime import datetime

class UserApi(Resource):
       def get(self,id):
              print("Inside get of USer api") 
              return "<h1>Hello! World</h1>"
              
       def put(self,id):
              print("Inside put of USer Apt")

       def post(self):
              data = request.get_json(force=True)  # or without force if header is set correctly

              try:
                     dob_obj = datetime.strptime(data['dob'], "%Y-%m-%d").date()
              except ValueError:
                     return {"error": "DOB must be in YYYY-MM-DD format"}, 400

              new_user = User(
                     full_name=data['full_name'],
                     username=data['username'],
                     email=data['email'],
                     password=data['password'],
                     parents_email=data.get('parents_email'),
                     dob=dob_obj,
                     user_type=data['user_type'],
                     institute_id=data['institute_id'],
                     user_class=data.get('user_class')
                     )
              check_by_username=db.session.query(User).filter(User.username == new_user.username).first()
              check_by_email=db.session.query(User).filter(User.email == new_user.email).first()
              if check_by_username:
                     return {"error":"Username is already taken"}
              elif check_by_email:
                     return {"error":"Email is already in use"}
              elif new_user.username is None or new_user.username=="":
                     return {"error":"User name cannot be empty"}
              elif new_user.full_name is None or new_user.full_name=="":
                     return {"error":"Full name cannot be empty"}
              elif new_user.email is None or new_user.email=="":
                     return {"error":"Email cannot be empty"}
              
              db.session.add(new_user)
              db.session.commit()

              return {"message": "User created successfully"   }, 201

       def delete(self,id):
              print("Inside delte of USer Api")