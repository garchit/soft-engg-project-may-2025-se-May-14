from models.user import User
from models import db



def to_dict(institute,total_students):
              return {"id":institute.id,"name":institute.name,"email":institute.email,"total_students":total_students}

def count_students(institute_id):
        return len(db.session.query(User).filter(User.institute_id==institute_id).all())