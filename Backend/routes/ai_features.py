from .recommended_courses import recommend_courses_semantic
from flask_restful import  Resource
from models.unit import Unit as Course
from models.user_course import UserCourse
from models import db
from transformers import pipeline


class RecommendedCourses(Resource):
    def get(self,user_id):
        courses=db.session.query(Course).all()
        all_courses={}

        for course in courses:
            all_courses[course.title]=course.description
        completed_courses_id=db.session.query(UserCourse).filter(UserCourse.user_id==user_id)
        completed_courses=[]
        for course_user in completed_courses_id:
            course=db.session.query(Course).filter(Course.id==course_user.course_id).first()
            completed_courses.append(course.title)
        recommended = recommend_courses_semantic(completed_courses, all_courses)
        
        return {"Recommended_Courses":recommended}
    

# Initialize once at startup
generator = pipeline('text-generation', model='microsoft/DialoGPT-medium')

def generate_ai_response_hf(prompt):
    response = generator(prompt, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']


