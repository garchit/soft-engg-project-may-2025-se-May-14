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
from flask_login import login_user, logout_user, login_required, current_user


class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)

            # Validate input
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return {"error": "Username and password are required."}, 400

            # Find the user
            user = User.query.filter_by(username=username).first()

            if not user:
                return {"error": "No such user."}, 404

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
    # @login_required
    def post(self):
        try:
            # logout_user()
            return {'message': 'Logout successful'}, 200
        except Exception as e:
            return {'error': f'Logout failed: {str(e)}'}, 500
        
        

