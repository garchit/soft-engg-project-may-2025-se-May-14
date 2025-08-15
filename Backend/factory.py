from flask import Flask
from extension import login_manager
from flasgger import Swagger
from flask_cors import CORS
from flask_migrate import Migrate
from extension import db 
from routes import init_routes
from models.user import User
from models.institute import Institute
from flask_swagger_ui import get_swaggerui_blueprint
from config import SWAGGER_URL, API_URL

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user:
        return user
    institute = Institute.query.get(int(user_id))
    if institute:
       return institute
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return {'error': 'Authentication required. Please log in.'}, 401
    
def create_app():
    app = Flask(__name__)   
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,     
        config={'app_name': "SAVVY API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    login_manager.init_app(app)
    login_manager.login_view = 'loginresource'

    init_routes(app)
    return app