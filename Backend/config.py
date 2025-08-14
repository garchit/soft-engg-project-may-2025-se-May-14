import os

SECRET_KEY = 'secretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(basedir, 'db_directory')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(DB_DIR, 'database.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
TESTING = False
REMEMBER_COOKIE_SAMESITE = "None"
REMEMBER_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = False
WTF_CSRF_ENABLED = False
SWAGGER_URL = '/api/docs'
API_URL = '/static/documentation.yaml'



# config.py

class Config:
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    
    SMTP_SERVER = 'localhost'     # MailHog or your real SMTP server
    SMTP_PORT = 1025              # MailHog default port
    FROM_EMAIL = 'savvyapp@study.in'
    PDFKIT_CONFIG = None 
    # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")



