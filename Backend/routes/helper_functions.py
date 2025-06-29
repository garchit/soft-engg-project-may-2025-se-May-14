from models.user import User
from models import db
from models.lecture import Lecture
from models.unit import Unit



def to_dict(institute,total_students):
              return {"id":institute.id,"name":institute.name,"email":institute.email,"total_students":total_students}

def count_students(institute_id):
        return len(db.session.query(User).filter(User.institute_id==institute_id).all())
def create_json(course):
    lectures=db.session.query(Lecture).filter(Lecture.unit_id==course.id).all()
    lecture_data=[]
    for lecture in lectures:
        lecture_data.append({"lecture_id":lecture.id,"lecture_title":lecture.title,
                             "lecture_description":lecture.description,
                             "lecture_link":lecture.link})
    
    return {"course_id":course.id,
            "course_title":course.title,
            "course_description":course.description,
            "lectures":lecture_data
            }