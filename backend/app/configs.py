# file to manage configs

# imports
import os
from dotenv import load_dotenv


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
    MAIL_USERNAME = (
        os.environ.get("mail_username") or None
    )  # os.environ["mail_username"] to be uncommented on live server
    MAIL_PASSWORD = (
        os.environ.get("mail_password") or None
    )  # os.environ["mail_password"] to be uncommented on live server

    CELERY = {
        "broker_url": "redis://localhost:6379",
        "result_backend": "redis://localhost:6379",
    }
