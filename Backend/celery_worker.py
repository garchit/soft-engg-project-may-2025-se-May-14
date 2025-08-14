from celery import Celery
from datetime import timedelta
from factory import create_app
from config import Config

# Create the Flask app
flask_app = create_app()

# Create the Celery app
celery = Celery(
    flask_app.import_name,
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
    include=["tasks"]
)

# Load Flask config into Celery
celery.conf.update(flask_app.config)

# Ensure tasks run inside Flask app context
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

# Celery Beat schedule for periodic tasks
celery.conf.beat_schedule = {
    # Send class reports every 30 seconds
    'class-report-every-30-sec': {
        'task': 'tasks.send_monthly_class_reports_to_teachers',
        'schedule': timedelta(seconds=30),
    },
}

celery.conf.timezone = 'Asia/Kolkata'
