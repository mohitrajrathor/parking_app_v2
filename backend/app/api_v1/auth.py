# handle auth related api logic

# imports
from flask_smorest import Blueprint, abort
from flask import current_app, render_template, request, url_for
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jwt_identity,
)
from ..extensions import db, mail, cache
from ..models import Admin, User
from ..schema import UserLoginSchema, TokenSchema, AdminLoginSchema, UserSignupSchema
from ..exceptions import APIError
from flask_mail import Message
from datetime import datetime as dt
import os
from ..utils import generate_confirmation_email, role_required


auth_bp = Blueprint(
    "auth", __name__, url_prefix="/auth", description="Authorization apis."
)


##### routes #####
@auth_bp.route("/test")
def auth_test():
    """
    Test route for the auth blueprint.

    Returns a simple string to verify the authentication routes are working.
    """
    return "testing -> auth test route"


@auth_bp.route("/admin-login", methods=["POST"])
@auth_bp.arguments(AdminLoginSchema, location="json")
@auth_bp.response(200, TokenSchema)
def admin_login(args):
    """
    Handles admin login by validating credentials and returning JWT access and refresh tokens upon successful authentication.

    Args:
        args (dict): JSON payload containing 'username' and 'password'.

    Returns:
        dict: Contains 'role', 'token', and 'refresh_token' on success.

    Raises:
        APIError: If admin is not found or password is incorrect.
        ValidationError: If input validation fails.
        500 error: For unexpected server errors.
    """
    try:
        admin = Admin.query.filter_by(username=args["username"]).first()
        if not admin:
            raise APIError("Admin not found!")

        if not admin.check_password(args["password"]):
            raise APIError("Wrong password", 401)

        return {
            "role": "admin",
            "token": create_access_token(
                identity=admin.id, additional_claims={"role": "admin"}
            ),
            "refresh_token": create_refresh_token(
                identity=admin.id, additional_claims={"role": "admin"}
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
    Authenticate a user with email and password.

    Accepts user credentials in JSON format, verifies the user, and returns access and refresh tokens on successful login.
    Returns an error if authentication fails.
    """
    try:

        user = User.query.filter_by(email=args["email"]).first()

        if not user:
            raise APIError("User not found!")

        if not user.check_password(args["password"]):
            raise APIError("Wrong password", 401)

        return {
            "message": "Login success!",
            "role": "user",
            "token": create_access_token(
                identity=user.id, additional_claims={"role": "user"}
            ),
            "refresh_token": create_refresh_token(
                identity=user.id, additional_claims={"role": "user"}
            ),
        }

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
    Handle user signup by creating a new user account, sending an email confirmation, and returning authentication tokens.

    Accepts user details in JSON format, validates input, checks for existing users, hashes the password, and sends a confirmation email.
    Returns access and refresh tokens upon successful registration.
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
            html=generate_confirmation_email(
                link=url_for(
                    "api_v1.auth.confirm_mail",
                    token=create_refresh_token(identity=user.email),
                    _external=True,
                )
            ),
        )

        mail.send(msg)

        db.session.add(user)
        db.session.commit()

        return {
            "message": "Signup complete, please confirm your email !",
            "role": "user",
            "token": create_access_token(
                identity=user.id, additional_claims={"role": "user"}
            ),
            "refresh_token": create_refresh_token(
                identity=user.id, additional_claims={"role": "user"}
            ),
        }

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@auth_bp.route("/send-confirm-mail", methods=["POST"])
@role_required("user")
def send_confirm_mail():
    """
    Send a confirmation email to the authenticated user for email verification.

    Requires the user role. Retrieves the current user from the JWT, generates a confirmation link, and sends an email with the verification link. Handles errors with appropriate responses.
    """
    try:
        id = get_jwt_identity()

        user = User.query.get(id)

        if not id or not user:
            raise APIError("bad token", 404)

        msg = Message(
            subject="Confirm you email",
            recipients=[user.email],
            sender="admin@parkly.com",
            body=f"welcome to parkly.com, to confirm mail follow this link {url_for("api_v1.auth.confirm_mail", token=create_refresh_token(identity=user.email))}",
            html=generate_confirmation_email(
                link=url_for(
                    "api_v1.auth.confirm_mail",
                    token=create_refresh_token(identity=user.email),
                    _external=True,
                )
            ),
        )

        mail.send(msg)

        return {
            "message": f"Confirmation mail sent to {user.email}, please check your inbox!",
            "status": "ok",
        }

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@auth_bp.route("/confirm-mail")
def confirm_mail():
    """
    Endpoint to confirm a user's email address using a token.

    Retrieves the token from the request, decodes it to get the user's email,
    verifies the user exists, marks the email as confirmed, and commits the change.
    Returns a success message and decoded email on success, or an error response on failure.
    """
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
