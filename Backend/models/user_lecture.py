from extension import db

class UserLecture(db.Model):
    __tablename__ = 'user_lecture'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id', ondelete='CASCADE'), primary_key=True)
    
