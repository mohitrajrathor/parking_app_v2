# analytics related routes

# imports
from flask_smorest import Blueprint, abort
from ..extensions import db
from ..models import Parking, Slot, User
from ..exceptions import APIError
from flask import current_app
from ..utils import role_required


analytics_bp = Blueprint(
    "analytics", __name__, url_prefix="/analytics", description="analytics related routes"
)


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

