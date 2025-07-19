# analytics related routes

# imports
from flask_smorest import Blueprint, abort
from ..extensions import db, cache
from ..models import Parking, Slot, User, Reservation, Review, Payment
from ..exceptions import APIError
from flask import current_app, jsonify, request
from ..utils import role_required
from sqlalchemy import func
from datetime import datetime, timedelta
import requests
from pprint import pprint
from ..schema import QuerySchema


analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/analytics",
    description="analytics related routes",
)


##### analytics functions ######
def get_top_parkings():
    top_parkings = (
        db.session.query(
            Parking.id.label("parking_id"),
            Parking.name,
            func.count(Reservation.id).label("reservation_count"),
        )
        .join(Reservation, Parking.id == Reservation.parking_id)
        .group_by(Parking.id, Parking.name)
        .order_by(func.count(Reservation.id).desc())
        .limit(3)
        .all()
    )

    # Correct unpacking
    top_parkings = [
        {"parking_id": parking_id, "name": name, "reservation_count": reservation_count}
        for parking_id, name, reservation_count in top_parkings
    ]

    return top_parkings


def get_last_30_days_revenue():
    today = datetime.now()
    start_date = today - timedelta(days=29)

    results = (
        db.session.query(
            func.date(Payment.payment_time).label("date"),
            func.coalesce(func.sum(Payment.amount), 0).label("revenue"),
        )
        .filter(Payment.payment_time >= start_date)
        .group_by(func.date(Payment.payment_time))
        .order_by(func.date(Payment.payment_time))
        .all()
    )

    daily_revenue = {
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): 0.0 for i in range(30)
    }

    for row in results:
        date_str = row.date if hasattr(row, "date") else row[0]
        revenue = row.revenue if hasattr(row, "revenue") else row[1]
        daily_revenue[date_str] = float(revenue)

    return daily_revenue


def get_profession_wise_user():
    """
    Return profession-wise user distribution data as a dict:
    {
        "Student": 120,
        "Engineer": 80,
        ...
    }
    """
    results = (
        db.session.query(User.profession, func.count(User.id))
        .group_by(User.profession)
        .all()
    )
    profession_dist = {
        profession if profession else "Unknown": count for profession, count in results
    }
    return profession_dist


def get_last_12_months_monthly_users():
    """
    Returns a dict of user signups per month for the last 12 months.
    Example:
    {
      "2024-08": 10,
      "2024-09": 15,
      ...
      "2025-07": 22
    }
    """
    today = datetime.now().replace(day=1)
    months = [
        (today - timedelta(days=30 * i)).strftime("%Y-%m") for i in reversed(range(12))
    ]
    # Get first day of each month
    month_starts = [
        datetime(today.year, today.month, 1) - timedelta(days=30 * i)
        for i in reversed(range(12))
    ]
    # Get last day of each month
    month_ends = [
        (month_starts[i + 1] if i < 11 else today + timedelta(days=31))
        - timedelta(days=1)
        for i in range(12)
    ]
    monthly_counts = {month: 0 for month in months}
    for i, month in enumerate(months):
        start = month_starts[i]
        end = month_ends[i]
        count = (
            db.session.query(func.count(User.id))
            .filter(User.join_time >= start, User.join_time <= end)
            .scalar()
        )
        monthly_counts[month] = count
    return monthly_counts


def get_last_30_days_daily_reservations():
    today = datetime.now()
    start_date = today - timedelta(days=29)

    results = (
        db.session.query(
            func.date(Reservation.start_time).label("date"),
            func.count(Reservation.id).label("reservation_count"),
        )
        .filter(Reservation.start_time >= start_date)
        .group_by(func.date(Reservation.start_time))
        .order_by(func.date(Reservation.start_time))
        .all()
    )

    daily_reservations = {
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): 0 for i in range(30)
    }

    for row in results:
        date_str = row.date if hasattr(row, "date") else row[0]
        reservation_count = (
            row.reservation_count if hasattr(row, "reservation_count") else row[1]
        )
        daily_reservations[date_str] = int(reservation_count)

    return daily_reservations


def get_user_age_distribution():
    """
    Compute user age distribution
    """
    age_bins = {
        "18-24": (18, 24),
        "25-34": (25, 34),
        "35-44": (35, 44),
        "45-54": (45, 54),
        "55-64": (55, 64),
        "65+": (65, 200),
    }
    age_distribution = {key: 0 for key in age_bins}
    today = datetime.now().date()
    users = db.session.query(User.dob).filter(User.dob != None).all()
    for (dob,) in users:
        if dob:
            age = (today - dob).days // 365
            for label, (min_age, max_age) in age_bins.items():
                if min_age <= age <= max_age:
                    age_distribution[label] += 1
                    break

    return age_distribution


@analytics_bp.route("/quick_stats", methods=["GET"])
@role_required("admin")
def quick_stats():
    """
    Get quick stats for the admin dashboard
    """
    try:
        # get total number of parking lots
        return {
            "total_parkings": Parking.query.count(),
            "total_slots": Slot.query.count(),
            "occupied_slots": Slot.query.filter_by(is_occupied=True).count(),
            "total_users": User.query.count(),
        }

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(f"Error getting quick stats: {e}")
        abort(500, message="Internal server error")


@analytics_bp.route("/databoard_analytics")
@role_required("admin")
def dashboard_analytics():
    """
    Get Dashboard analytics data.
    """
    try:
        return jsonify(
            avg_rating=round(db.session.query(func.avg(Review.rating)).scalar(), 1),
            active_bookings=Reservation.query.filter_by(is_booked=True).count(),
            total_reservations=Reservation.query.count(),
            total_revenue=round(db.session.query(func.sum(Payment.amount)).scalar(), 2),
            total_reviews=Review.query.count(),
            booking_revenue=round(
                db.session.query(func.sum(Payment.amount))
                .filter(Payment.pay_for == "booking")
                .scalar(),
                2,
            ),
            top_parkinsg=get_top_parkings(),
            daily_revenue=get_last_30_days_revenue(),
            total_slots=Slot.query.count(),
            booked_slots=Slot.query.filter_by(is_occupied=True).count(),
        )

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@analytics_bp.route("/parking_analytics")
def parking_analytics():
    """
    Return parking analytics data
    """
    try:
        return jsonify(daily_reservations=get_last_30_days_daily_reservations()), 200

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(f"Reverse geocode error: {e}")
        return jsonify({"address": "Unknown address"}), 500


@analytics_bp.route("/user_analytics")
@role_required("user", "admin")
def user_analytics():
    """
    Return parking analytics data
    """
    try:
        return (
            jsonify(
                age_dist=get_user_age_distribution(),
                monthly_user_growth=get_last_12_months_monthly_users(),
                profession_dist=get_profession_wise_user(),
            ),
            200,
        )

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(f"Reverse geocode error: {e}")
        return jsonify({"address": "Unknown address"}), 500


@analytics_bp.route("/reverse_geocode", methods=["GET"])
@cache.cached(timeout=60, query_string=True)
def reverse_geocode():
    """
    Proxy endpoint for reverse geocoding using Nominatim OpenStreetMap API.
    Accepts lat and long as query params.
    """
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not lat or not lon:
        return abort(400, message="Missing lat or lon query parameter.")
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
        headers = {"User-Agent": "parking-app-proxy/1.0"}
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        pprint(data)
        return jsonify({"address": data.get("display_name", "Unknown address")})

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(f"Reverse geocode error: {e}")
        return jsonify({"address": "Unknown address"}), 500
