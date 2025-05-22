# handle auth related api logic

# imports
from flask_smorest import Blueprint, abort
from flask import current_app
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from ..extensions import db
from ..models import Admin, User
from ..schema import UserLoginSchema, TokenSchema, AdminLoginSchema
from ..exceptions import APIError


auth_bp = Blueprint(
    "auth", __name__, url_prefix="/auth", description="Authorization apis."
)


##### routes #####
@auth_bp.route("/test")
def auth_test():
    return "testing -> auth test route"


@auth_bp.route("/admin/login", methods=["POST"])
@auth_bp.arguments(AdminLoginSchema, location="form")
@auth_bp.response(200, TokenSchema)
def admin_login(args):
    """
    admin login
    """
    try:
        admin = Admin.query.filter_by(username=args["username"]).first()
        if not admin:
            raise APIError("Admin not found!")

        if not admin.check_password(args["password"]):
            raise APIError("Wrong password", 401)

        return {
            "role": "admin",
            "token": create_access_token(identity={"role": "admin", "id": admin.id}),
            "refresh_token": create_refresh_token(
                identity={"role": "admin", "id": admin.id}
            ),
        }

    except ValidationError as e:
        current_app.logger.error(e)
        return abort(
            404, message="Field validation failed", additional_data={"details": str(e)}
        )

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@auth_bp.route("/login", methods=["POST"])
@auth_bp.arguments(UserLoginSchema, location="form")
@auth_bp.response(200, TokenSchema)
def user_login(args):
    """
    user login
    """
    try:
        user = User.query.filter_by(email=args["email"]).first()
        if not user:
            raise APIError("User not found!")

        if not user.check_password(args["password"]):
            raise APIError("Wrong password", 401)

        return {
            "role": "user",
            "token": create_access_token(identity={"role": "user", "id": user.id}),
            "refresh_token": create_refresh_token(
                identity={"role": "user", "id": user.id}
            ),
        }

    # except ValidationError as e:
    #     current_app.logger.error(e)
    #     return abort(
    #         404, message="Field validation failed", additional_data={"details": str(e)}
    #     )

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@auth_bp.route("/signup")
def signup():
    pass
