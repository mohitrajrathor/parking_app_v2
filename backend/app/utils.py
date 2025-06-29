# utility logic

# imports
from .extensions import db
from functools import wraps
from typing import List
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify


def create_models():
    from .models import Admin, User, Parking, Slot, Review, Payment

    db.create_all()


def populate():
    from .populate import (
        add_Admin,
        add_test_user,
        add_test_parking_and_slots,
        add_test_payment,
        add_test_reservation,
        add_test_review,
    )

    add_Admin()
    add_test_user()
    add_test_parking_and_slots()
    add_test_reservation()
    add_test_review()
    add_test_payment()


def role_required(*allowed_roles):
    """
    decorator for role based access control

    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            role = claims.get("role", None)
            if role not in allowed_roles:
                return jsonify({"msg": "Access forbidden: insufficient role"}), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator


def generate_confirmation_email(link):
    """
    To generate html for emial varification.

    """
    return f"""
    <html>
    <body style="font-family: sans-serif; color: #333;">
        <h2>Confirm your email</h2>
        <p>Click the link below to verify your email for Parkly:</p>
        <p><a href="{link}">{link}</a></p>
        <p>If you didn’t request this, you can ignore this email.</p>
        <p>– Parkly Team</p>
    </body>
    </html>
    """
