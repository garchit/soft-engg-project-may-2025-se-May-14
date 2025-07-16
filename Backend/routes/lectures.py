from flask import request
from flask_restful import Resource
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.lecture import Lecture
from models.unit import Unit  # required to check if unit_id exists
from models.user_lecture import UserLecture
from models.user import User


class LectureResource(Resource):

    @login_required
    def get(self, id):
        lecture = db.session.query(Lecture).filter(Lecture.id == id).first()
        if not lecture:
            return {"error": "Lecture not found"}, 404

        return {
            "message": "Lecture Found",
            "id": lecture.id,
            "unit_id": lecture.unit_id,
            "title": lecture.title,
            "description": lecture.description,
            "link": lecture.link
        }, 200

    # @login_required
    def post(self):
        data = request.get_json(force=True)
        title = data.get("title")
        description = data.get("description")
        link = data.get("link")
        unit_id = data.get("unit_id")

        if not title or not unit_id:
            return {"error": "Title and Unit ID are required"}, 400

        # Check if unit exists
        unit = db.session.get(Unit, unit_id)
        if not unit:
            return {"error": "Invalid unit_id. No such unit exists."}, 400

        try:
            # Prevent duplicate title in the same unit
            existing = db.session.query(Lecture).filter_by(title=title, unit_id=unit_id).first()
            if existing:
                return {"error": "Lecture with this title already exists in the unit"}, 400

            new_lecture = Lecture(
                title=title,
                description=description,
                link=link,
                unit_id=unit_id
            )
            db.session.add(new_lecture)
            db.session.flush()  # Ensures ID is generated before commit
            lecture_id = new_lecture.id
            db.session.commit()

            return {"message": "Lecture added successfully", "id": lecture_id}, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Internal Server Error", "details": str(e)}, 500

    @login_required
    def put(self, id):
        data = request.get_json(force=True)
        title = data.get("title")
        description = data.get("description")
        link = data.get("link")
        unit_id = data.get("unit_id")

        # Validate unit existence
        unit = db.session.get(Unit, unit_id)
        if not unit:
            return {"error": "Invalid unit_id. No such unit exists."}, 400

        # Prevent duplicate title in same unit (except current lecture)
        check_title = db.session.query(Lecture).filter(
            Lecture.id != id,
            Lecture.title == title,
            Lecture.unit_id == unit_id
        ).first()
        if check_title:
            return {"error": "Lecture title already exists in the unit"}, 400

        lecture = db.session.query(Lecture).filter(Lecture.id == id).first()
        if not lecture:
            return {"error": "Lecture not found"}, 404

        try:
            lecture.title = title
            lecture.description = description
            lecture.link = link
            lecture.unit_id = unit_id
            db.session.commit()

            return {
                "message": "Lecture updated successfully",
                "title": title,
                "description": description,
                "link": link,
                "unit_id": unit_id
            }, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Internal Server Error", "details": str(e)}, 500

    @login_required
    def delete(self, id):
        try:
            lecture = db.session.query(Lecture).filter(Lecture.id == id).first()
            if not lecture:
                return {"error": "Lecture not found"}, 404

            db.session.delete(lecture)
            db.session.commit()
            return {"message": "Lecture deleted successfully"}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Internal Server Error", "details": str(e)}, 500
        
class UserLectureResource(Resource):
    def get(self):
        pass
    def post(self,user_id,lecture_id):
        user=db.session.query(User).filter(User.id==user_id).first()
        if user:
            lecture=db.session.query(Lecture).filter(Lecture.id==lecture_id).first()
            if lecture:
                user_lecture=UserLecture(user_id=user_id,lecture_id=lecture_id)
                db.session.add(user_lecture)
                db.session.commit()
                return {
                    "message":"Succesfully Watched Lecture"
                },200


        
        
        
