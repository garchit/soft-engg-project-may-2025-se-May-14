from models import db

class Institute(db.Model):
    __tablename__ = 'institute'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address=db.Column(db.String(255), nullable=False)