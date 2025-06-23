from flask import request
from flask_restful import Resource
from models import db
from models.lecture import Lecture
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required

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

    @login_required
    def post(self):
        data = request.get_json(force=True)
        title = data.get("title")
        description = data.get("description")
        link = data.get("link")
        unit_id = data.get("unit_id")

        if not title or not unit_id:
            return {"error": "Title and Unit ID are required"}, 400

        try:
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
            db.session.commit()
            return {"message": "Lecture added successfully", "id": new_lecture.id}, 201

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

        check_title = db.session.query(Lecture).filter(Lecture.id != id, Lecture.title == title, Lecture.unit_id == unit_id).first()
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
