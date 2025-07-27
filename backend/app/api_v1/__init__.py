# api version 1 module

# imports
from flask_smorest import Blueprint


api_v1 = Blueprint(
    "api_v1",
    __name__,
    url_prefix="/api_v1",
    description="API version 1 for Parkly. This blueprint aggregates all v1 endpoints including authentication, parking, analytics, user management, reservations, and background tasks.",
)


###### sub blueprints ######
from .auth import auth_bp
from .test import test_bp
from .parking import parking_bp
from .analytics import analytics_bp
from .user import user_bp
from .reservations import reserve_bp
from .task_routes import task_bp

api_v1.register_blueprint(auth_bp)
api_v1.register_blueprint(test_bp)
api_v1.register_blueprint(parking_bp)
api_v1.register_blueprint(analytics_bp)
api_v1.register_blueprint(user_bp)
api_v1.register_blueprint(reserve_bp)
api_v1.register_blueprint(task_bp)


##### routes ######
@api_v1.route("/test")
@api_v1.doc(
    description="Test endpoint for API version 1. Returns a simple string to verify the API is working.",
    summary="API v1 Test Endpoint",
    responses={
        200: {
            "description": "A simple test response confirming API v1 is operational.",
            "content": {
                "text/plain": {"example": "testing -> api version 1 test route"}
            },
        }
    },
    tags=["Test"],
)
def api_v1_test():
    """
    Test endpoint for API version 1.

    Returns:
        str: Confirmation string that API v1 is operational.
    """
    return "testing -> api version 1 test route"
