from celery import Celery
from celery.schedules import crontab
from factory import create_app
from config import Config


flask_app = create_app()


celery = Celery(
    flask_app.import_name,
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
    include=["tasks"]  
)

celery.conf.update(flask_app.config)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask


celery.conf.beat_schedule = {
    'send-monthly-teacher-reports': {
        'task': 'tasks.send_monthly_class_reports_to_teachers',

        'schedule': crontab(minute='*/2'), 

        # 'schedule': timedelta(days=30),
    },
    'schedule-weekly-parent-reports': {
        'task': 'tasks.schedule_all_parent_reports',

        'schedule': crontab(minute='*/2'),

        # 'schedule': timedelta(weeks=1),
    }
}


celery.conf.timezone = 'Asia/Kolkata'