# file to manage configs

# imports
import os
from dotenv import load_dotenv


class Config:
    load_dotenv()

    SECRET_KEY = os.environ["secret_key"]
    SQLALCHEMY_DATABASE_URI = "sqlite:///parking.db"

    #### CORS
    ORIGIN = "*"

    #### JWT
    JWT_SECRET_KEY = os.environ["secret_key"]
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 30  # in sec now 30 min
    JWT_REFRESH_TOKEN_EXPIRES = 60 * 60 * 24 * 7  # in 7 days

    #### Mail
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None  # os.environ["mail_username"] to be uncommented on live server
    MAIL_PASSWORD = None  # os.environ["mail_password"] to be uncommented on live server

    CELERY = {
        "broker_url": "redis://localhost:6379",
        "result_backend": "redis://localhost:6379",
    }
