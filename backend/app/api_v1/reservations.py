# api module to handle reservations

# imports
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from datetime import datetime as dt
from zoneinfo import ZoneInfo
from ..extensions import db
from ..models import Reservation, Parking, User, Review, Payment, Slot
from ..exceptions import APIError
from flask import current_app, request
from ..utils import role_required
from flask_jwt_extended import get_jwt_identity


# blueprint
reserve_bp = Blueprint(
    "Reservation",
    __name__,
    description="Operations on reservations",
    url_prefix="/reservation",
)


class ReservationSchema(Schema):
    parking_id = fields.Int()
    reservation_id = fields.Int()


@reserve_bp.route("", methods=["POST"])
@reserve_bp.arguments(ReservationSchema)
@role_required("user")
def book_slot(args):
    """
    to reserve a slot
    """
    try:
        print(request.json)
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
