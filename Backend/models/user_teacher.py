from extension import db

class UserTeacher(db.Model):
    __tablename__ = 'user_teacher'

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),primary_key=True)
    teacher_id = db.Column(db.Integer,db.ForeignKey('teachers.id'),nullable=False)

