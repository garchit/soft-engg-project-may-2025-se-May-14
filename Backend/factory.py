from flask import Flask
from extension import login_manager
from flasgger import Swagger
from flask_cors import CORS
from flask_migrate import Migrate
from models import db,init_db
from routes import init_routes
# from flask_restful import APi
from models.user import User
from flask_swagger_ui import get_swaggerui_blueprint
from config import SWAGGER_URL, API_URL

# login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
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

    # migrate = Migrate(app, db)
    # init_db(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    init_routes(app)
    return app