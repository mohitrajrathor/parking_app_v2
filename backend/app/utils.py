# CSV report makers for user monthly and all-time reports
import io
import csv


def monthly_report_to_csv(report_data):
    """
    Takes the dict output of User.monthly_report(), validates, and returns an in-memory CSV file object.
    """
    if not report_data or "bookings" not in report_data:
        raise ValueError("Invalid report data: missing bookings list")

    output = io.StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(
        [
            "Reservation ID",
            "Parking Name",
            "Slot Serial",
            "Start Time",
            "Leave Time",
            "Hours Used",
            "Is Booked",
            "Payments",
        ]
    )

    for booking in report_data["bookings"]:
        payments_str = "; ".join(
            [
                f"{p['pay_for']} {p['amount']} at {p['paid_at']}"
                for p in booking.get("payments", [])
            ]
        )
        writer.writerow(
            [
                booking.get("reservation_id"),
                booking.get("parking_name"),
                booking.get("slot_serial"),
                booking.get("start_time"),
                booking.get("leave_time"),
                booking.get("hours_used"),
                booking.get("is_booked"),
                payments_str,
            ]
        )

    output.seek(0)
    return output


def all_time_report_to_csv(report_data):
    """
    Takes the dict output of User.all_time_report(), validates, and returns an in-memory CSV file object.
    """
    # Structure is the same as monthly_report, so we can reuse logic
    return monthly_report_to_csv(report_data)


# utility logic

# imports
from .extensions import db
from functools import wraps
from typing import List
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify
from math import radians, sin, cos, sqrt, atan2
import datetime as dt


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
        <p>If you didn't request this, you can ignore this email.</p>
        <p>– Parkly Team</p>
    </body>
    </html>
    """


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth surface.
    Args:
        lat1, lon1: Latitude and longitude of point 1 (in decimal degrees)
        lat2, lon2: Latitude and longitude of point 2 (in decimal degrees)
    Returns:
        Distance in kilometers (float)
    """
    R = 6371.0  # Earth radius in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def calculate_hours(start: dt.datetime, end: dt.datetime) -> float:
    """
    Calculate time difference in hours, rounded down to nearest 1 hour, minimum 1 hour.
    """
    delta = end - start
    hours = delta.total_seconds() / 3600
    rounded = round(hours)
    return rounded
