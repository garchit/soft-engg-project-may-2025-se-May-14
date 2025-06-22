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
from models.institute import Institute
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user


class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)

            # Validate input
            email = data.get("email")
            password = data.get("password")

            if not email or not password:

                return {"error": "Email and password are required."}, 400

            # Find the user
            user = User.query.filter_by(email=email).first()

            if not user:
                institute = Institute.query.filter_by(email=email).first()
                if not institute:
                    return {"error": "No such user."}, 404
                if institute.password!=password:
                    return {"error":"Invalid Credentials"},401
                login_user(institute)
                return {
                    "message":"Login is Successful",
                    "id":institute.id,
                    "name":institute.name
                }

            # Check password (plain text comparison)
            if user.password != password:
                return {"error": "Wrong password. Invalid credentials."}, 401

            # Login successful
            login_user(user)
            return {
                "message": "Login is successful",
                "user": {
                    "id": user.id,
                    "username": user.username
                    # Add other fields if needed
                }
            }, 200

        except Exception as e:
            # Log the error or print it for debugging
            return {"error": f"Something went wrong: {str(e)}"}, 500
        
class LogoutResource(Resource):
    @login_required
    def post(self):
        try:
            # logout_user()
            return {'message': 'Logout successful'}, 200
        except Exception as e:
            return {'error': f'Logout failed: {str(e)}'}, 500
        
        

