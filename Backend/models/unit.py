from extension import db

class Unit(db.Model):
    __tablename__ = 'unit'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    lectures = db.relationship('Lecture', backref='unit', cascade='all, delete-orphan')
    questions=db.relationship('Question',backref='unit',cascade="all,delete-orphan")