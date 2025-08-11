from models.badges import Badge
from models.user import User
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from models import db

class BadgeResourse(Resource):
    def get(self,id=None):
        try:
            if id== None:
                badges=db.session.query(Badge).all()
                badge_list=[]
                for badge in badges:
                    badge_list.append({"id":badge.id,"name":badge.name,"description":badge.description})
                return {"list_badges":badge_list},200
            else:
                badge = db.session.query(Badge).filter_by(id=id).first()
            if not badge:
                return {"message": f"Badge with id {id} not found."}, 404

            return {
                "id": badge.id,
                "name": badge.name,
                "description": badge.description,
                "points": badge.points
            }, 200
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error.", "details": str(e)}, 500
        


    def put(self,id):
        if id==None:
            return {"message": "Badge ID is required for update."}, 400
        try:
            data = request.get_json(force=True)

            # Validate input
            if not data:
                return {"message": "Request body is missing or invalid JSON."}, 400

            # Extract fields with default None
            name = data.get("name")
            description = data.get("description")
            points = data.get("points")

            # Check required fields
            if name is None or description is None or points is None:
                return {"message": "Fields 'name', 'description', and 'points' are required."}, 400

            # Optional: validate points type
            if not isinstance(points, int) or points < 0:
                return {"message": "'points' must be a non-negative integer."}, 400

            # Find badge
            badge = db.session.query(Badge).filter(Badge.id==id).first()
            if not badge:
                return {"message": f"Badge with id {id} not found."}, 404

            # Update fields
            badge.name = name
            badge.description = description
            badge.points = points

            db.session.commit()

            return {
                "message": f"Badge {id} successfully updated.",
                "badge": {
                    "id": badge.id,
                    "name": badge.name,
                    "description": badge.description,
                    "points": badge.points
                }
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error occurred.", "error": str(e)}, 500

        except Exception as e:
            return {"message": "An unexpected error occurred.", "error": str(e)}, 500
        
    def post(self):
        try:
            data = request.get_json(force=True)
        except Exception:
            return {"error": "Invalid JSON payload."}, 400

        # Validate required fields
        name = data.get('name')
        description=data.get('description')
        points = data.get('points')

        if not name:
            return {"error": "'name' field is required."}, 400
        if points is None:
            return {"error": "'points' field is required."}, 400
        if not isinstance(points, int):
            return {"error": "'points' must be an integer."}, 400

        # Check for duplicate badge name
        if Badge.query.filter_by(name=name).first():
            return {"error": f"Badge with name '{name}' already exists."}, 400

        # Try creating and saving the badge
        try:
            badge = Badge(name=name, points=points,description=description)
            db.session.add(badge)
            db.session.commit()

            return {
                "message": "Badge created successfully.",
                "badge": {
                    "id": badge.id,
                    "name": badge.name,
                    "points": badge.points,
                    "description":description
                }
            }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error.", "details": str(e)}, 500

        except Exception as e:
            return {"error": "An unexpected error occurred.", "details": str(e)}, 500

    def delete(self, id):
        try:
            # Look up badge by ID
            badge = db.session.query(Badge).filter(Badge.id==id).first()
            if not badge:
                return {"message": f"Badge with id {id} not found."}, 404

            # Delete badge
            db.session.delete(badge)
            db.session.commit()

            return {"message": f"Badge {id} successfully deleted."}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error occurred.", "error": str(e)}, 500

        except Exception as e:
            return {"message": "An unexpected error occurred.", "error": str(e)}, 500
            
