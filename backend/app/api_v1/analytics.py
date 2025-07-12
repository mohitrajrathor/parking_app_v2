# analytics related routes

# imports
from flask_smorest import Blueprint, abort
from ..extensions import db
from ..models import Parking, Slot, User, Reservation, Review, Payment
from ..exceptions import APIError
from flask import current_app, jsonify
from ..utils import role_required
from sqlalchemy import func, cast, Date
from datetime import datetime, timedelta


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

    except Exception as e:
        current_app.logger.error(f"Error getting quick stats: {e}")
        abort(500, message="Internal server error")


@analytics_bp.route("/databoard_analytics")
# @role_required("admin")
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

    # except Exception as e:
    #     current_app.logger.error(e)
    #     return abort(500, message="Internal Server Error.")
