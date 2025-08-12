from flask import request
from flask_restful import Resource
from models.institute import Institute
from models.teacher import Teacher
from extension import db
from models.user import User
from .helper_functions import overall_progress
from sqlalchemy.exc import SQLAlchemyError
from .log_in_out import role_required
from sqlalchemy import func 

class Homepage(Resource):
    def get(self):
        """Get the homepage data for admin dashboard
        Returns:total institutes, total teachers, total students, and institute-wise performance"""
        try:
            total_institutes=db.session.query(Institute).count()
            total_teachers=db.session.query(Teacher).count()
            total_students=db.session.query(User).filter(User.user_type==0).count()
            count_class=count_users_by_class()

            institute_info=[]
            for institute in db.session.query(Institute).all():
                average_score=institute_wise_progress(institute_id=institute.id)
                institute_info.append({
                    "institute_id": institute.id,
                    "institute_name": institute.name,
                    "average_score": round(average_score*100,2),
                    "performance": "Good" if average_score >= 75 else "Average" if average_score >= 50 else "Poor"
                })
            return {"total_institutes":total_institutes,
                    "total_teachers":total_teachers,
                    "total_students":total_students,
                    "count_class":count_class,
                    "institute_info":institute_info}, 200
        except SQLAlchemyError as e:
            return {"error":"internal server error","details":str(e)},500
        
def institute_wise_progress(institute_id):
        """Get the average progress of students in a specific institute
        Args: institute_id (int): ID of the institute
        Returns: average progress of students in the institute"""
        try:
                progress=0
                students=db.session.query(User).filter(User.institute_id==institute_id).all()
                for student in students:
                    user_id=student.id
                    if user_id:
                        # Assuming overall_progress is a function that calculates the progress for a user
                        progress+=overall_progress(user_id=user_id)
                total_students=len(students)
                if total_students > 0:
                    average_score=progress/total_students
                    return average_score
                else:
                    return 0
                    
        except SQLAlchemyError as e:
            return {"error":"internal server error","details":str(e)},500
    
def count_users_by_class():
    results = (
        db.session.query(User.user_class, func.count(User.id)).filter(User.user_class.isnot(None))
        .group_by(User.user_class)
        .all()
    )
    return {user_class: count for user_class, count in results}