from flask import request
from flask_restful import Resource
from datetime import datetime
from models import db
from models.user import User

class UserApi(Resource):
    def get(self, id):
        user = db.session.query(User).filter(User.id == id).first()
        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "full_name": user.full_name,
            "username": user.username,
            "email": user.email,
            "parents_email": user.parents_email,
            "dob": str(user.dob),
            "user_type": "admin" if user.user_type else "student",
            "institute_id": user.institute_id,
            "user_class": user.user_class
        }, 200

    def post(self):
        data = request.get_json(force=True)

        try:
            dob_obj = datetime.strptime(data['dob'], "%Y-%m-%d").date()
        except ValueError:
            return {"error": "DOB must be in YYYY-MM-DD format"}, 400

        role = data.get("user_type")
        if role == "admin":
            user_type = True
        elif role == "student":
            user_type = False
        else:
            return {"error": "Invalid user_type. Use 'student' or 'admin'"}, 400

        if db.session.query(User).filter(User.username == data['username']).first():
            return {"error": "Username is already taken"}, 400
        if db.session.query(User).filter(User.email == data['email']).first():
            return {"error": "Email is already in use"}, 400

        if not data['username']:
            return {"error": "Username cannot be empty"}, 400
        if not data['full_name']:
            return {"error": "Full name cannot be empty"}, 400
        if not data['email']:
            return {"error": "Email cannot be empty"}, 400

        new_user = User(
            full_name=data['full_name'],
            username=data['username'],
            email=data['email'],
            password=data['password'],
            parents_email=data.get('parents_email'),
            dob=dob_obj,
            user_type=user_type,
            institute_id=data['institute_id'],
            user_class=data.get('user_class')
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

    def put(self, id):
        user = db.session.query(User).filter(User.id == id).first()
        if not user:
            return {"error": "User not found"}, 404

        data = request.get_json()

        user.full_name = data.get('full_name', user.full_name)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.parents_email = data.get('parents_email', user.parents_email)
        user.user_class = data.get('user_class', user.user_class)

        role = data.get("user_type", "admin" if user.user_type else "student")
        if role == "admin":
            user.user_type = True
        elif role == "student":
            user.user_type = False
        else:
            return {"error": "Invalid user_type. Use 'student' or 'admin'"}, 400

        if 'dob' in data:
            try:
                user.dob = datetime.strptime(data['dob'], "%Y-%m-%d").date()
            except ValueError:
                return {"error": "DOB must be in YYYY-MM-DD format"}, 400

        db.session.commit()
        return {"message": "User updated successfully"}, 200

    def delete(self, id):
        user = db.session.query(User).filter(User.id == id).first()
        if not user:
            return {"error": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
