# extensions management code

# imports
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from flask_smorest import Api
from flask_caching import Cache
from celery import Celery, Task
from flask import Flask
import os


# extension instances
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()
cors = CORS()
api = Api()
cache = Cache()


# celery setup
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.conf.update(app.config.get("CELERY", {}))
    celery_app.conf.beat_schedule = app.config.get("CELERY_BEAT_SCHEDULE", {})
    celery_app.set_default()

    celery_app.conf.timezone = "Asia/Kolkata"
    celery_app.autodiscover_tasks(["app"])
    app.extensions["celery"] = celery_app

    return celery_app
