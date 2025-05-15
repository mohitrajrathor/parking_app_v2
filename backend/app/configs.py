# file to manage configs

# imports
import os
from dotenv import load_dotenv


class Config:
    load_dotenv()

    SECRET_KEY = os.environ["secret_key"]
    SQLALCHEMY_DATABASE_URI = "sqlite:///parking.db"
