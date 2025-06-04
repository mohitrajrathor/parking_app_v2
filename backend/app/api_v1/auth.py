# handle auth related api logic

# imports
from flask_smorest import Blueprint, abort
from flask import current_app, render_template, request, url_for
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    jwt_required,
    get_jwt_identity,
)
from ..extensions import db
from ..models import Admin, User
from ..schema import UserLoginSchema, TokenSchema, AdminLoginSchema, UserSignupSchema
from ..exceptions import APIError
from ..extensions import mail
from flask_mail import Message
from datetime import datetime as dt
import os


auth_bp = Blueprint(
    "auth", __name__, url_prefix="/auth", description="Authorization apis."
)


##### routes #####
@auth_bp.route("/test")
def auth_test():
    return "testing -> auth test route"


@auth_bp.route("/admin-login", methods=["POST"])
@auth_bp.arguments(AdminLoginSchema, location="json")
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
@auth_bp.arguments(UserLoginSchema, location="json")
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


@auth_bp.route("/signup", methods=["POST"])
@auth_bp.arguments(UserSignupSchema, location="json")
@auth_bp.response(200, TokenSchema)
def signup(args):
    """
    user signup route
    """

    try:
        if User.query.filter_by(email=args["email"]).first():
            raise APIError("User already exist", status_code=401)

        user = User(
            email=args["email"],
            name=args["name"],
            dob=dt.strptime(args["dob"], "%Y-%m-%d"),
            profession=args["profession"],
            address=args["address"],
            pincode=args["pincode"],
            phone=args["phone"],
        )

        user.set_password(args["password"])

        # sending email confirmation mail.
        msg = Message(
            sender="admin@parkly.com",
            subject="Confirm you email",
            recipients=[user.email],
            body=f"welcome to parkly.com, to confirm mail follow this link {url_for("api_v1.auth.confirm_mail", token=create_refresh_token(identity=user.email), _external=True)}",
            html=render_template(
                "confirmation_mail.html",
                confirmation_link=url_for(
                    "api_v1.auth.confirm_mail",
                    token=create_refresh_token(identity=user.email),
                    _external=True,
                ),
            ),
        )

        mail.send(msg)

        db.session.add(user)
        db.session.commit()

        return {
            "role": "user",
            "token": create_access_token(identity={"role": "user", "id": user.id}),
            "refresh_token": create_refresh_token(
                identity={"role": "user", "id": user.id}
            ),
        }

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@auth_bp.route("/send-confirm-mail", methods=["POST"])
@jwt_required()
def send_confirm_mail():
    try:
        identity = get_jwt_identity()
        id = identity.get("id")

        user = User.query.get(id)

        if not identity or not user:
            raise APIError("bad token", 404)

        msg = Message(
            subject="Confirm you email",
            recipients=[user.email],
            body=f"welcome to parkly.com, to confirm mail follow this link {url_for("api_v1.auth.confirm_mail", token=create_refresh_token(identity=user.email))}",
            html=render_template(
                "confirmation_mail.html",
                confirmation_link=url_for(
                    "api_v1.auth.confirm_mail",
                    token=create_refresh_token(identity=user.email),
                ),
            ),
        )

        mail.send(msg)

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@auth_bp.route("/confirm-mail")
def confirm_mail():
    try:
        token = request.args.get("token")
        if not token:
            raise APIError("invalid token or token not found!", status_code=404)

        email = decode_token(token)["sub"]

        user = User.query.filter_by(email=email).first()

        if not user:
            raise APIError("no such email exist!", 404)

        user.email_confirmed = True

        db.session.commit()

        return {"message": "email confirmed", "decoded_data": email}, 200

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")
