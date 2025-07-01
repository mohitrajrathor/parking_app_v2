# api version 1 module

# imports
from flask_smorest import Blueprint





api_v1 = Blueprint("api_v1", __name__, url_prefix="/api_v1")


###### sub blueprints ######
from .auth import auth_bp
from .test import test_bp
from .parking import parking_bp
from .analytics import analytics_bp
from .user import user_bp
from .reservations import reserve_bp

api_v1.register_blueprint(auth_bp)
api_v1.register_blueprint(test_bp)
api_v1.register_blueprint(parking_bp)
api_v1.register_blueprint(analytics_bp)
api_v1.register_blueprint(user_bp)
api_v1.register_blueprint(reserve_bp)



##### routes ######
@api_v1.route("/test")
def api_v1_test():
    return "testing -> api version 1 test route"
