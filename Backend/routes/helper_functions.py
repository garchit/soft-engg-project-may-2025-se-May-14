from models.user import User
from extension import db
from models.lecture import Lecture
from models.unit import Unit
from models.user_lecture import UserLecture
from models.lecture import Lecture
from models.unit import Unit as Course
from models.user_course import UserCourse
from models.teacher import Teacher
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func


def to_dict(institute,total_students):
              return {"id":institute.id,"name":institute.name,"email":institute.email,"total_students":total_students,
                      "blocked":institute.blocked
                      }

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

def lecture_progress(user_id,course_id):
        total_lectures=db.session.query(Lecture).filter(Lecture.unit_id==course_id).all()
        total_lectures_attempted=0
        for lecture in total_lectures:
                user_lecture=db.session.query(UserLecture).filter(UserLecture.user_id==user_id,UserLecture.lecture_id==lecture.id).first()
                if user_lecture:
                        total_lectures_attempted+=1
        if len(total_lectures)!=0:
                attempted_quiz=len(db.session.query(UserCourse).filter(UserCourse.user_id==user_id,UserCourse.course_id==course_id).all())
                # print(attempted_quiz)
                progress=round(((total_lectures_attempted)*100)/len(total_lectures),2)
        else:
                progress=0
        return {course_id:progress}

def course_progress(user_id):
        total_progress=[]
        courses=db.session.query(Course).all()
        for course in courses:
                total_progress.append((lecture_progress(user_id=user_id,course_id=course.id)))
                total_progress[-1][course.id]=0.7*total_progress[-1][course.id]
                completed_course=db.session.query(UserCourse).filter(UserCourse.user_id==user_id,UserCourse.course_id==course.id).first()
                if completed_course:
                        total_progress[-1][course.id]=round(total_progress[-1][course.id]+30,2)
        return total_progress


def overall_progress(user_id):
        course_total_progress=course_progress(user_id)
        sum_progress=0
        for progress in course_total_progress:
            sum_progress+=list(progress.values())[0]
        total_courses=db.session.query(Course).count()
        overall_progress=sum_progress/total_courses
        return round(overall_progress,2)

def getTeachers(institute_id):
        teachers=db.session.query(Teacher).filter(Teacher.institute_id==institute_id)
        ids=[]
        for teacher in teachers:
                ids.append(teacher.id)
        return ids

def getTeacherName(teacher_id):
       teacher = db.session.query(Teacher).filter(Teacher.id==teacher_id).first()
       
       if teacher: return teacher.name
       else: return "No teacher"
def user_score(user_id):
    try:
        # Check if user exists
        user = db.session.query(User).filter(User.id == user_id).first()
        if not user:
            print(f"User with id {user_id} not found.")
            return 0

        # Get total score (if summing over multiple courses)
        total_score = db.session.query(func.sum(UserCourse.marks_scored)).filter(UserCourse.user_id == user_id).scalar()
        print(f"Total score for user {user_id}: {total_score}") #debugging line
        # If no score is found, return 0

        return total_score or 0

    except SQLAlchemyError as e:
        db.session.rollback()
        return {"error": "Database error occurred", "details": str(e)}, 500

    except Exception as e:
        return {"error": "Unexpected error occurred", "details": str(e)}, 500

def average_institute_score(institute_id):
        try:
               users=db.session.query(User).filter(User.institute_id==institute_id).all()
               if not users:
                     return 0
               total_score = 0
               for user in users:
                      score=user_score(user.id)
                      total_score += score
               average_score = total_score / len(users)
               return round(average_score, 2)

        except SQLAlchemyError as e:
               db.session.rollback()
               return {"error": "Database error occurred", "details": str(e)}, 500        
        #        return 0

def get_unit_name(unit_id):
       return db.session.query(Course).filter(Course.id == unit_id).first().title