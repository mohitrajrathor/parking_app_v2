# extensions management code

# imports
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from flask_smorest import Api
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


# celery setup
def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()

    # to make all task autodetactable by celery
    task_modlues = ["app.tasks"] + [
        "app.tasks." + task.split(".")[0]
        for task in os.listdir(os.path.join(app.root_path, "tasks"))
        if os.path.isfile(os.path.join(app.root_path, "tasks", task))
        and not task == "__init__.py"
    ]

    celery_app.autodiscover_tasks(task_modlues)
    app.extensions["celery"] = celery_app

    return celery_app
