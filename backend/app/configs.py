# file to manage configs

# imports
import os
from dotenv import load_dotenv
from celery.schedules import crontab


class Config:
    load_dotenv()

    SECRET_KEY = os.environ["secret_key"]
    SQLALCHEMY_DATABASE_URI = "sqlite:///parking.db"

    #### smorest setup
    API_TITLE = "Parly api documentation"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/docs"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        "security": [{"bearerAuth": []}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
    }

    #### CORS
    ORIGIN = "*"

    #### JWT
    JWT_SECRET_KEY = os.environ["secret_key"]
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 30  # in sec now 30 min
    JWT_REFRESH_TOKEN_EXPIRES = 60 * 60 * 24 * 7  # in 7 days

    #### Mail
    MAIL_SERVER = os.environ.get("mail_server") or "localhost"
    MAIL_PORT = os.environ.get("mail_port") or 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get("mail_username") or None
    MAIL_PASSWORD = os.environ.get("mail_password") or None

    CELERY = {
        "broker_url": "redis://localhost:6379",
        "result_backend": "redis://localhost:6379",
    }

    CELERY_BEAT_SCHEDULE = {
        "run-demo-every-minute": {
            "task": "app.tasks.demo",  # fully qualified task name
            "schedule": 60.0,  # in seconds (every 60 seconds)
            # OR use crontab
            # "schedule": crontab(minute="*/1"),  # every 1 minute
            "args": (),  # optional
        },
        "send-daily-reminders": {
            "task": "app.tasks.daily_remainders",
            "schedule": crontab(hour=8, minute=0),  # every day at 8:00 AM
            "args": (),  # optional
        },
    }

    ##### Cache
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = os.environ.get("CACHE_REDIS_HOST", "localhost")
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = f"redis://{CACHE_REDIS_HOST}:{CACHE_REDIS_PORT}/{CACHE_REDIS_DB}"
