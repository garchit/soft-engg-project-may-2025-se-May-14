from models import db

class Lecture(db.Model):
    __tablename__ = 'lectures'
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id', ondelete='CASCADE'), nullable=False)
    link = db.Column(db.Text)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)