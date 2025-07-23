# api module to handle reservations

# imports
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from datetime import datetime as dt
from zoneinfo import ZoneInfo
from ..extensions import db, cache
from ..models import Reservation, Parking, User, Review, Payment, Slot
from ..exceptions import APIError
from flask import current_app, request
from ..utils import role_required, calculate_hours
from flask_jwt_extended import get_jwt_identity
from ..schema import QuerySchema, IdSchema

# blueprint
reserve_bp = Blueprint(
    "Reservation",
    __name__,
    description="Operations on reservations",
    url_prefix="/reservation",
)


class ReservationSchema(Schema):
    """
    Schema for serializing and deserializing reservation data, including parking, reservation IDs, leave time, feedback, and rating.
    """

    parking_id = fields.Integer()
    reservation_id = fields.Integer()
    leave_time = fields.DateTime()
    feedback = fields.Str()
    rating = fields.Integer()


@reserve_bp.route("/by_id", methods=["GET"])
@reserve_bp.arguments(IdSchema, location="query")
@role_required("user", "admin")
def get_by_id(args):
    """
    Retrieve reservation details by reservation ID.

    Requires 'user' or 'admin' role. Returns reservation data as a dictionary if found,
    otherwise raises an APIError. Handles errors and logs exceptions.
    """
    try:
        id = args.get("id", None)
        if not id:
            raise APIError("No reservation found", 404)

        reservation = Reservation.query.get(int(id))
        return reservation.to_dict()

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@reserve_bp.route("", methods=["GET"])
@reserve_bp.arguments(QuerySchema, location="query")
@role_required("user", "admin")
def get(args):
    """
    Retrieve a paginated list of reservations filtered by parking name.

    Args:
        args (dict): Query parameters including 'page', 'per_page', and optional 'query' for filtering.

    Returns:
        dict: Paginated reservation data with metadata and serialized reservation details.

    Raises:
        APIError: If a custom API error occurs.
        500 error: For unexpected server errors.
    """
    try:
        page = args.get("page", 1)
        per_page = args.get("per_page", 10)

        query_str = args.get("query", "")
        reservations = (
            Reservation.query.join(Parking, Reservation.parking_id == Parking.id)
            .filter(Parking.name.ilike(f"%{query_str}%"))
            .paginate(page=page, per_page=per_page)
        )

        return {
            "total": reservations.total,
            "page": reservations.page,
            "pages": reservations.pages,
            "has_next": reservations.has_next,
            "has_prev": reservations.has_prev,
            "reservations": [rsvsn.to_dict() for rsvsn in reservations],
        }

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@reserve_bp.route("", methods=["POST"])
@reserve_bp.arguments(ReservationSchema)
@role_required("user")
def book_slot(args):
    """
    Handle POST request to reserve a parking slot for a user.

    Checks for available slots in the specified parking,
    creates a reservation and payment record,
    and returns booking and payment details.
    Handles errors for invalid parking IDs, unavailable slots, and internal exceptions.
    """
    try:
        parking = Parking.query.get(args.get("parking_id"))
        user = User.query.get(get_jwt_identity())

        if not parking:
            raise APIError("Parking id is invalid!", 404)

        slot = Slot.query.filter_by(parking_id=parking.id, is_occupied=False).first()

        if not slot:
            raise APIError("No Slot is free, Sorry for inconvinience!", 409)

        # booking slot
        slot.is_occupied = True

        reserve = Reservation(
            user_id=user.id, parking_id=parking.id, slot_id=slot.id, is_booked=True
        )

        db.session.add(reserve)
        db.session.commit()

        pay = Payment(
            user_id=user.id,
            parking_id=parking.id,
            reserve_id=reserve.id,
            fee=parking.booking_fee,
            amount=parking.booking_fee,
            payment_time=dt.now(ZoneInfo("Asia/Kolkata")),
            pay_for="booking",
        )

        db.session.add(pay)
        db.session.commit()

        return {
            "message": "Slot booked successfully.",
            "reservation_id": reserve.id,
            "payment_details": {
                "payer": user.name,
                "parking": parking.name,
                "fee": parking.booking_fee,
                "amount": pay.amount,
                "slot_alloted": slot.serial_id,
                "payment_time": pay.payment_time.strftime("%d-%m-%yT%H:%M%S"),
            },
        }, 200

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@reserve_bp.route("", methods=["PUT"])
@reserve_bp.arguments(ReservationSchema)
@role_required("user")
def leave_slot(args):
    """
    Handles the process for a user to leave a reserved parking slot.
    Updates reservation and slot status, records payment for parking duration, and creates a review.
    Validates input, manages timezones, and returns payment and reservation details on success.
    """
    try:
        print(request.json)
        reservation = Reservation.query.get(args.get("reservation_id"))
        user = User.query.get(get_jwt_identity())
        parking = Parking.query.get(args["parking_id"])
        feedback = args.get("feedback", None)
        rating = args.get("rating", None)

        if not feedback or not rating:
            raise APIError("Review is required !", 409)

        if not parking:
            raise APIError("Parking id is not valid !", 404)

        if not reservation:
            raise APIError("Reservation id is invalid!", 404)

        slot = Slot.query.get(reservation.slot_id)

        if not slot:
            raise APIError("Slot is invalid conflict!", 409)

        # Validate leave_time (handle ISO 8601 with/without Z)
        leave_time_raw = args["leave_time"]
        if isinstance(leave_time_raw, dt):
            leave_time = leave_time_raw
        else:
            # Handle 'Z' (UTC) at the end of the string
            if isinstance(leave_time_raw, str) and leave_time_raw.endswith("Z"):
                leave_time = dt.fromisoformat(leave_time_raw.replace("Z", "+00:00"))
            else:
                leave_time = dt.fromisoformat(leave_time_raw)
        # Convert leave_time to Asia/Kolkata timezone if it's not already
        if leave_time.tzinfo is None:
            leave_time = leave_time.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
        else:
            leave_time = leave_time.astimezone(ZoneInfo("Asia/Kolkata"))
        # Ensure reservation.start_time is also timezone-aware in Asia/Kolkata
        start_time = reservation.start_time
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
        else:
            start_time = start_time.astimezone(ZoneInfo("Asia/Kolkata"))
        if leave_time < start_time:
            raise APIError("Leave time cannot be before start time!", 400)

        # Free slot and update reservation
        slot.is_occupied = False
        reservation.is_booked = False
        reservation.leave_time = leave_time
        db.session.commit()

        # Use leave_time for hours calculation
        hours_parked = calculate_hours(start=start_time, end=leave_time)
        cost_amt = parking.hourly_fee * hours_parked

        pay = Payment(
            user_id=user.id,
            parking_id=reservation.parking.id,
            reserve_id=reservation.id,
            fee=reservation.parking.booking_fee,
            amount=cost_amt,
            payment_time=dt.now(ZoneInfo("Asia/Kolkata")),
            pay_for="leave",
        )

        db.session.add(pay)
        db.session.commit()

        review = Review(
            user_id=user.id,
            parking_id=parking.id,
            reservation_id=reservation.id,
            feedback=feedback,
            rating=rating,
        )
        db.session.add(review)
        db.session.commit()

        return {
            "message": "Slot left successfully.",
            "reservation_id": reservation.id,
            "payment_id": pay.id,
            "payment_details": {
                "payer": user.name,
                "parking": parking.name,
                "fee": parking.booking_fee,
                "amount": cost_amt,
                "slot_leaved": slot.serial_id,
                "payment_time": pay.payment_time.strftime("%d-%m-%yT%H:%M%S"),
            },
        }, 200

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")
