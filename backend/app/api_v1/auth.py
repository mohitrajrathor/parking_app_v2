# handle auth related api logic

# imports
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


##### routes #####
@auth_bp.route("/test")
def auth_test():
    return "testing -> auth test route"
