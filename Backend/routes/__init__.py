from flask_restful import Api
from .user import UserApi
from .log_in_out import LoginResource,LogoutResource
from .institute_resource import InstituteResource,AllInstitute
from .teachers_resource import TeacherResource
from .unit_resource import CourseResource
from .lectures import LectureResource
from .questions_resource import QuestionResource
from .questions_resource import AllQuestionResource
from .streak_resource import StreakResource,StreakCalendarData


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
    api.add_resource(AllQuestionResource, '/questions/unit/<int:unit_id>')
    api.add_resource(StreakResource,'/user/streak')
    api.add_resource(StreakCalendarData,'/user/streak/calendar')

