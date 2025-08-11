from flask import request
from flask_restful import Resource
from datetime import datetime
from models import db
from models.user import User
from models.institute import Institute
from sqlalchemy.exc import SQLAlchemyError
from models.user_teacher import UserTeacher
from models.teacher import Teacher
from .log_in_out import role_required
from flask_login import login_required

class UserApi(Resource):
    # @role_required(0)
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
            "user_class": user.user_class,
            "password": user.password
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
        user.parents_email = data.get('parents_email', user.parents_email)

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
    
class VerifyStudents(Resource):
    def get(self, institute_id):
        try:
            institute = db.session.query(Institute).filter_by(id=institute_id).first()
            if not institute:
                return {
                    "message": f"Institution with id {institute_id} does not exist.",
                    "students": []
                }, 404
            students = db.session.query(User).filter(
                User.institute_id == institute_id,
                User.verified == 0
            ).all()

            unverified_student_list = [
                {
                    "id": student.id,
                    "name": student.full_name,
                    "class":student.user_class,
                    "dob": str(student.dob)
                }
                for student in students
            ]

            return {
                "message": "Successfully fetched unverified students.",
                "students": unverified_student_list
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": "Database error occurred.",
                "error": str(e)
            }, 500

        except Exception as e:
            return {
                "message": "An unexpected error occurred.",
                "error": str(e)
            }, 500
    def put(self, user_id):
        try:
            data = request.get_json(force=True)

            # Validate input
            if not data or "verified" not in data:
                return {"message": "Missing 'verified' field in request body."}, 400

            verified_value = data["verified"]
            if verified_value not in [1, -1]:
                return {"message": "Invalid value for 'verified'. Must be 1 (verify) or -1 (reject)."}, 400

            # Check if user exists
            user = db.session.query(User).filter_by(id=user_id).first()
            if not user:
                return {"message": f"User with id {user_id} not found."}, 404

            # Update verified status
            user.verified = verified_value
            institute_id,user_class=user.institute_id,user.user_class

            
            teacher = db.session.query(Teacher).filter(Teacher.class_teacher == user_class,Teacher.institute_id == institute_id).first()

            if not teacher:
                return {"message": "No teacher found for the given class and institute."}, 404

            user_teacher = UserTeacher(user_id=user_id,teacher_id=teacher.id)
            db.session.add(user_teacher)
            db.session.commit()

            status = "verified" if verified_value == 1 else "rejected"
            return {
                "message": f"User {user_id} has been successfully {status}."
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                "message": "Database error occurred.",
                "error": str(e)
            }, 500

        except Exception as e:
            return {
                "message": "An unexpected error occurred.",
                "error": str(e)
            }, 500