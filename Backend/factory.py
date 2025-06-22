from flask import Flask
from flask_login import LoginManager
from flasgger import Swagger
from flask_cors import CORS
from flask_migrate import Migrate
from models import db,init_db
from routes import init_routes
# from flask_restful import APi
from models.user import User

login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    CORS(app)
    # migrate = Migrate(app, db)
    # init_db(app)
    login_manager.init_app(app)

    init_routes(app)
    return app