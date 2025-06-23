from flask_restful import Api
from .user import UserApi
from .log_in_out import LoginResource,LogoutResource
from .institute_resource import InstituteResource
from .teachers_resource import TeacherResource
from .unit_resource import UnitResource
from lectures import LectureResource

def init_routes(app):
    api = Api(app, prefix='/Finance_Tutor')

    # USer Route
    api.add_resource(UserApi,"/User/signup","/User/<int:id>")
    api.add_resource(LoginResource,"/login")
    api.add_resource(LogoutResource,"/logout")
    api.add_resource(InstituteResource,"/institute/<int:id>","/institute/signup")
    api.add_resource(TeacherResource,"/teacher","/teacher/<int:id>")
    api.add_resource(UnitResource,"/unit","/unit/<int:id>")
    api.add_resource(LectureResource, '/lecture', '/lecture/<int:id>')


    