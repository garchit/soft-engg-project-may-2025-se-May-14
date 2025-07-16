from models import db

class UserCourse(db.Model):
    __tablename__ = 'user_course'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('unit.id', ondelete='CASCADE'), primary_key=True)
    marks_scored=db.Column(db.Integer)
