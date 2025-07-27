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
    description="Analytics related routes for parking, revenue, user demographics, and dashboard statistics.",
)


##### analytics functions ######
def get_top_parkings():
    """
    Retrieve the top 3 parkings with the highest number of reservations.

    Returns:
        list: A list of dictionaries, each containing the parking ID, name, and reservation count.
    """
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
    """
    Calculates and returns a dictionary of daily revenue totals for the last 30 days.

    Returns:
        dict: Keys are date strings in 'YYYY-MM-DD' format, values are total revenue (float) for each day.
    """
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
    Retrieve a dictionary representing the distribution of users by profession.

    Returns:
        dict: Keys are profession names (or "Unknown" if not specified), values are user counts.
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
    Retrieve the number of user signups for each of the last 12 months.

    Returns:
        dict: A dictionary mapping each month (YYYY-MM) to the count of users who joined in that month.
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
    """
    Returns a dictionary of daily reservation counts for the last 30 days.

    Queries the Reservation table to count the number of reservations for each day,
    starting from 29 days ago up to today. Dates with no reservations are included
    with a count of zero.

    Returns:
        dict: Keys are date strings in 'YYYY-MM-DD' format, values are reservation counts.
    """
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
    Calculate and return the distribution of users across predefined age groups.

    Returns:
        dict: A dictionary mapping age group labels to the number of users in each group.
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
@analytics_bp.doc(
    summary="Get quick admin dashboard statistics",
    description="Retrieve quick statistics for the admin dashboard, including total parkings, total slots, occupied slots, and total users.",
    tags=["Dashboard", "Admin", "Quick Stats"],
    responses={
        200: {
            "description": "Quick statistics for dashboard.",
            "content": {
                "application/json": {
                    "example": {
                        "total_parkings": 10,
                        "total_slots": 200,
                        "occupied_slots": 50,
                        "total_users": 100,
                    }
                }
            },
        },
        500: {"description": "Internal Server Error."},
    },
)
@role_required("admin")
def quick_stats():
    """
    Retrieve quick statistics for the admin dashboard, including total parkings, total slots, occupied slots, and total users.
    """
    try:
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
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@analytics_bp.route("/databoard_analytics")
@analytics_bp.doc(
    summary="Get admin dashboard analytics",
    description="Returns aggregated dashboard analytics data for admins, including average rating, active bookings, total reservations, total revenue, total reviews, booking revenue, top parkings, daily revenue for the last 30 days, total slots, and booked slots.",
    tags=["Dashboard", "Admin", "Analytics"],
    responses={
        200: {"description": "Aggregated dashboard analytics data."},
        500: {"description": "Internal Server Error."},
    },
)
@role_required("admin")
def dashboard_analytics():
    """
    Returns aggregated dashboard analytics data for admins, including average rating, active bookings, total reservations, total revenue, total reviews, booking revenue, top parkings, daily revenue for the last 30 days, total slots, and booked slots.
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
@analytics_bp.doc(
    summary="Get daily parking reservation analytics for the last 30 days",
    description="Returns daily reservation counts for the last 30 days as a JSON object.",
    tags=["Analytics", "Parking", "Reservations"],
    responses={
        200: {
            "description": "Daily reservation counts for the last 30 days.",
            "content": {
                "application/json": {
                    "example": {
                        "daily_reservations": {"2025-07-01": 5, "2025-07-02": 7}
                    }
                }
            },
        },
        500: {"description": "Internal Server Error."},
    },
)
def parking_analytics():
    """
    Handles the /parking_analytics route and returns daily parking reservation analytics for the last 30 days as JSON.

    Returns:
        Response: JSON object with daily reservation counts and HTTP status code.
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
@analytics_bp.doc(
    summary="Get user analytics (age, growth, profession)",
    description="Returns user analytics including age distribution, monthly user growth, and profession distribution.",
    tags=["Analytics", "User"],
    responses={
        200: {
            "description": "User analytics data.",
            "content": {
                "application/json": {
                    "example": {
                        "age_dist": {"18-24": 10, "25-34": 20},
                        "monthly_user_growth": {"2025-07": 5, "2025-06": 3},
                        "profession_dist": {"Engineer": 15, "Doctor": 5},
                    }
                }
            },
        },
        500: {"description": "Internal Server Error."},
    },
)
@role_required("user", "admin")
def user_analytics():
    """
    Retrieve aggregated parking analytics data for users, including age distribution, monthly user growth, and profession distribution.

    Returns:
        Response: JSON object containing analytics data with HTTP status 200 on success, or an error response on failure.
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
@analytics_bp.doc(
    summary="Reverse geocode latitude and longitude to address",
    description="Proxies a request to the Nominatim OSM API to resolve latitude and longitude to a human-readable address. Caches results for 24 hours.",
    tags=["Analytics", "Geocoding"],
    responses={
        200: {
            "description": "Resolved address for given coordinates.",
            "content": {
                "application/json": {
                    "example": {"address": "Some Street, Some City, Country"}
                }
            },
        },
        400: {"description": "Missing lat or lon query parameter."},
        500: {"description": "Internal Server Error."},
    },
)
@cache.cached(timeout=(60 * 60 * 24), query_string=True)
def reverse_geocode():
    """
    Handles GET requests to proxy reverse geocoding using the Nominatim OSM API.

    Accepts 'lat' and 'lon' as query parameters and returns the resolved address.
    Caches responses for 60 seconds based on query string.
    Returns 400 if required parameters are missing, and 500 on unexpected errors.
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
