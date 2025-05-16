# extensions management code

# imports
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS


# extension instances
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()
cors = CORS()
