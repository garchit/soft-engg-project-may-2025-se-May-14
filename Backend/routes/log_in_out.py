from flask import request, jsonify
from flask_restful import Resource
from extension import db
from models.user import User
from models.institute import Institute
from functools import wraps
from flask_login import login_user, logout_user, login_required, current_user

class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json(force=True)
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                return {"error": "Email and password are required."}, 400

            user = User.query.filter_by(email=email).first()

            if not user:
                institute = Institute.query.filter_by(email=email).first()
                if not institute:
                    return {"error": "No such user."}, 404
                if institute.password != password:
                    return {"error": "Invalid Credentials"}, 401
                
                # ✅ ADDED: remember=True to create a persistent session
                login_user(institute, remember=True)
                
                # ✅ ADJUSTED: Made the response consistent for the frontend
                return {
                    "message": "Login is Successful",
                    "user": {
                        "id": institute.id,
                        "username": institute.name,
                        "role": "institute"
                    }
                }

            if user.password != password:
                return {"error": "Wrong password. Invalid credentials."}, 401

            # ✅ ADDED: remember=True to create a persistent session
            login_user(user, remember=True)
            return {
                "message": "Login is successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "role": "admin" if user.user_type == 1 else "student"
                }
            }, 200

        except Exception as e:
            return {"error": f"Something went wrong: {str(e)}"}, 500

class LogoutResource(Resource):
    @login_required
    def post(self):
        try:
            logout_user()
            return {'message': 'Logout successful'}, 200
        except Exception as e:
            return {'error': f'Logout failed: {str(e)}'}, 500

class UserProfileResource(Resource):
    @login_required
    def get(self):
        if not isinstance(current_user, User):
            return {'error': 'Profile not available for this user type'}, 404
            
        return {
            'id': current_user.id,
            'full_name': current_user.username,
            'email': current_user.email,
            'role': 'admin' if current_user.user_type == 1 else 'student'
        }
        
def role_required(*roles):
    """A decorator to restrict access to users with specific roles."""
    def wrapper(fn):
        @wraps(fn)
        @login_required
        def decorated_view(*args, **kwargs):
            if not hasattr(current_user, 'user_type') or current_user.user_type not in roles:
                return jsonify({'message': 'Forbidden: You do not have the required role.'}), 403
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper