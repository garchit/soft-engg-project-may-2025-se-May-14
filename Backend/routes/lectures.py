from flask import request
from flask_restful import Resource
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from extension import db
from models.lecture import Lecture
from models.unit import Unit  # required to check if unit_id exists
from models.user_lecture import UserLecture
from models.user import User
from .badge_resource import check_and_award_badges


class LectureResource(Resource):

    # @login_required
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

            return {"message": "Lecture added successfully", "id": lecture_id,
                    "title": title, "description": description, "link": link, "unit_id": unit_id
                    }, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Internal Server Error", "details": str(e)}, 500

    # @login_required
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

    # @login_required
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
    def post(self, user_id, lecture_id):
        user = db.session.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "User not found"}, 404

        lecture = db.session.query(Lecture).filter(Lecture.id == lecture_id).first()
        if not lecture:
            return {"error": "Lecture not found"}, 404

        # Avoid duplicate UserLecture entry
        existing = db.session.query(UserLecture).filter_by(user_id=user_id, lecture_id=lecture_id).first()
        if existing:
            return {"message": "Lecture already watched"}, 200

        user_lecture = UserLecture(user_id=user_id, lecture_id=lecture_id)
        db.session.add(user_lecture)
        db.session.commit()

        # Check and award badges if criteria met
        newly_awarded_badges = check_and_award_badges(user_id)

        response_data = {"message": "Successfully watched lecture"}
        if newly_awarded_badges:
            response_data["new_badges"] = [{"name": b.name, "description": b.description} for b in newly_awarded_badges]

        return response_data, 200
    
    def get(self, user_id):
        """
        Retrieves all courses where the user has watched at least one lecture.
        
        This method performs a series of JOIN operations to link the user's
        watched lectures to their respective courses, ensuring a unique list of
        courses is returned.
        """
        # First, verify if the user exists
        user = db.session.query(User).filter(User.id == user_id).first()
        if not user:
            return {"error": "User not found"}, 404

        # Join from Unit -> Lecture -> UserLecture
        # and filter by the provided user_id
        watched_courses = (
            db.session.query(Unit)
            .join(Lecture, Unit.id == Lecture.unit_id)
            .join(UserLecture, Lecture.id == UserLecture.lecture_id)
            .filter(UserLecture.user_id == user_id)
            .distinct()
            .all()
        )

        # Handle the case where no courses with watched lectures are found
        if not watched_courses:
            return {"course_detail": [], "message": "No courses with watched lectures found"}, 200

        # Serialize the list of course objects into a dictionary format
        course_list = []
        for unit in watched_courses:
            course_list.append({
                "course_id": unit.id,
                "course_title": unit.title,
                "course_description": unit.description
            })

        return {"course_detail": course_list}, 200