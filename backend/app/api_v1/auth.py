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
from dotenv import load_dotenv


load_dotenv()

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    description="Authorization APIs for user and admin authentication, registration, email confirmation, and session management. Includes endpoints for login, signup, email verification, and token-based authentication.",
)


##### routes #####
@auth_bp.route("/test")
@auth_bp.doc(
    summary="Test authentication route",
    description="Test route for the auth blueprint. Returns a simple string to verify the authentication routes are working.",
    tags=["Auth", "Test"],
    responses={
        200: {
            "description": "Test route is working.",
            "content": {"text/plain": {"example": "testing -> auth test route"}},
        }
    },
)
def auth_test():
    """
    Test route for the auth blueprint.

    Returns a simple string to verify the authentication routes are working.
    """
    return "testing -> auth test route"


@auth_bp.route("/admin-login", methods=["POST"])
@auth_bp.doc(
    summary="Admin login",
    description="Handles admin login by validating credentials and returning JWT access and refresh tokens upon successful authentication.",
    tags=["Auth", "Admin"],
    responses={
        200: {"description": "Admin login successful, returns tokens."},
        401: {"description": "Invalid credentials."},
        404: {"description": "Admin not found."},
        500: {"description": "Internal Server Error."},
    },
)
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
@auth_bp.doc(
    summary="User login",
    description="Authenticate a user with email and password. Returns access and refresh tokens on successful login.",
    tags=["Auth", "User"],
    responses={
        200: {"description": "User login successful, returns tokens."},
        401: {"description": "Invalid credentials."},
        404: {"description": "User not found."},
        500: {"description": "Internal Server Error."},
    },
)
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
@auth_bp.doc(
    summary="User signup",
    description="Handle user signup by creating a new user account, sending an email confirmation, and returning authentication tokens.",
    tags=["Auth", "User"],
    responses={
        200: {"description": "Signup successful, returns tokens."},
        401: {"description": "User already exists."},
        500: {"description": "Internal Server Error."},
    },
)
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
        email_token = create_refresh_token(identity=user.email)

        # sending email confirmation mail.
        msg = Message(
            sender="admin@parkly.com",
            subject="Confirm you email",
            recipients=[user.email],
            body=f"welcome to parkly.com, to confirm mail follow this link {url_for("api_v1.auth.confirm_mail", token=email_token, _external=True)}",
            html=generate_confirmation_email(
                link=f"{os.environ.get("VITE_BASE_URL")}/verify-mail?token={email_token}"
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
@auth_bp.doc(
    summary="Send confirmation email",
    description="Send a confirmation email to the authenticated user for email verification.",
    tags=["Auth", "User", "Email"],
    responses={
        200: {"description": "Confirmation mail sent."},
        404: {"description": "Bad token or user not found."},
        500: {"description": "Internal Server Error."},
    },
    security=[{"BearerAuth": []}],
)
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

        email_token = create_refresh_token(identity=user.email)

        # sending email confirmation mail.
        msg = Message(
            sender="admin@parkly.com",
            subject="Confirm you email",
            recipients=[user.email],
            body=f"welcome to parkly.com, to confirm mail follow this link {url_for("api_v1.auth.confirm_mail", token=email_token, _external=True)}",
            html=generate_confirmation_email(
                link=f"{os.environ.get("VITE_BASE_URL")}/verify-mail?token={email_token}"
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
@auth_bp.doc(
    summary="Confirm user email",
    description="Endpoint to confirm a user's email address using a token. Marks the email as confirmed and returns tokens for login.",
    tags=["Auth", "User", "Email"],
    responses={
        200: {"description": "Email confirmed, returns tokens."},
        400: {"description": "Invalid token payload."},
        404: {"description": "Invalid token or user not found."},
        500: {"description": "Internal Server Error."},
    },
)
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
            raise APIError("Invalid token or token not found!", status_code=404)

        email = decode_token(token).get("sub")
        if not email:
            raise APIError("Invalid token payload!", status_code=400)

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "User with this email not found!"}, 404

        if not user.email_confirmed:
            user.email_confirmed = True
            db.session.commit()

        return {
            "message": "Email confirmed!",
            "role": "user",
            "token": create_access_token(
                identity=user.id, additional_claims={"role": "user"}
            ),
            "refresh_token": create_refresh_token(
                identity=user.id, additional_claims={"role": "user"}
            ),
        }, 200

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)
    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")
