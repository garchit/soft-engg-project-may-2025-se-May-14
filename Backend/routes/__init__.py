from flask_restful import Api
from .user import UserApi
from .log_in_out import LoginResource,LogoutResource
from .institute_resource import InstituteResource,AllInstitute,ToggleBlockInstitute
from .teachers_resource import TeacherResource,UserTeacherResource,TeacherWiseProgress
from .unit_resource import CourseResource,CompletedCourse,CourseProgress
from .lectures import LectureResource, UserLectureResource
from .questions_resource import QuestionResource
from .ai_features import RecommendedCourses



def init_routes(app):
    api = Api(app, prefix='/Finance_Tutor')

    # USer Route
    api.add_resource(UserApi,"/User/signup","/User/<int:id>")
    api.add_resource(LoginResource,"/login")
    api.add_resource(LogoutResource,"/logout")
    api.add_resource(InstituteResource,"/institute/<int:id>","/institute/signup")
    api.add_resource(TeacherResource,"/teacher","/teacher/<int:id>")
    api.add_resource(CourseResource,"/course","/course/<int:id>")
    api.add_resource(LectureResource, '/lecture', '/lecture/<int:id>')
    api.add_resource(AllInstitute, '/all_institute')
    api.add_resource(QuestionResource, '/question','/question/<int:id>')
    api.add_resource(ToggleBlockInstitute, '/toggle_block_institute/<int:institute_id>')
    api.add_resource(CompletedCourse, '/user_course_completed/<int:user_id>')
    api.add_resource(UserLectureResource, '/user_lecture_watched/<int:user_id>/<int:lecture_id>')
    api.add_resource(CourseProgress, '/course_progress/<int:user_id>')
    api.add_resource(UserTeacherResource,"/user_teacher/<int:user_id>")
    api.add_resource(TeacherWiseProgress,"/teacher_wise_progress/<int:institute_id>")
    api.add_resource(RecommendedCourses,"/recommended_courses/<int:user_id>")


