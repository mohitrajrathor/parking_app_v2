# api version 1 module

# imports
from flask_smorest import Blueprint


api_vi = Blueprint("api_v1", __name__, url_prefix="/api_v1")


###### sub blueprints ######
from .auth import auth_bp
from .test import test_bp
from .parking import parking_bp

api_vi.register_blueprint(auth_bp)
api_vi.register_blueprint(test_bp)
api_vi.register_blueprint(parking_bp)


##### routes ######
@api_vi.route("/test")
def api_v1_test():
    return "testing -> api version 1 test route"
