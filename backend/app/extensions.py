# extensions management code

# imports
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail


# extension instances
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()
