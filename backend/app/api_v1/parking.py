# parking related routes

# imports
from flask_smorest import Blueprint, abort
from ..schema import (
    QuerySchema,
    ParkingSchema,
    ParkingResponseSchema,
    ParkingWithSlothSchema,
    IdSchema,
    SlotQuerySchema,
)
from ..extensions import db
from ..models import Parking, Slot
from ..exceptions import APIError
from flask import current_app
from ..utils import role_required, haversine_distance

parking_bp = Blueprint(
    "parking", __name__, url_prefix="/parking", description="parking related routes"
)


@parking_bp.route("/by_id", methods=["GET"])
@parking_bp.arguments(IdSchema, location="query")
@parking_bp.response(200, ParkingWithSlothSchema)
def get_parking_id(args):
    """
    get parking by id
    """
    try:
        id = args.get("id")
        if not id:
            raise APIError("id must be given as query parameter!", 404)

        parking = Parking.query.get(id)
        if parking:
            return parking.to_dict()

        return {"message": "No parking found!"}, 404

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@parking_bp.route("", methods=["GET"])
@parking_bp.arguments(QuerySchema, location="query")
@parking_bp.response(200, ParkingResponseSchema)
def get_parking(args):
    """
    get parkings by query or latitude or longitude
    """
    try:
        page = args.get("page") or 1
        per_page = args.get("per_page") or 10

        if args.get("query"):
            parkings = Parking.query.filter(
                Parking.name.ilike(f"%{args.get('query')}%")
            ).paginate(page=page, per_page=per_page)

            return {
                "total": parkings.total,
                "page": parkings.page,
                "pages": parkings.pages,
                "has_next": parkings.has_next,
                "has_prev": parkings.has_prev,
                "parkings": [parking.to_dict() for parking in parkings],
            }

        if args.get("lat") and args.get("long"):
            user_lat = float(args.get("lat"))
            user_long = float(args.get("long"))
            all_parkings = Parking.query.all()
            parkings_with_distance = []
            for parking in all_parkings:
                distance = haversine_distance(
                    user_lat, user_long, parking.lat, parking.long
                )
                parkings_with_distance.append((parking, distance))
            parkings_with_distance.sort(key=lambda x: x[1])
            # Paginate manually
            start = (page - 1) * per_page
            end = start + per_page
            paginated = parkings_with_distance[start:end]
            return {
                "total": len(parkings_with_distance),
                "page": page,
                "pages": (len(parkings_with_distance) + per_page - 1) // per_page,
                "has_next": end < len(parkings_with_distance),
                "has_prev": start > 0,
                "parkings": [
                    p[0].to_dict() | {"distance_km": round(p[1], 2)} for p in paginated
                ],
            }

        parkings = Parking.query.paginate(page=page, per_page=per_page)

        return {
            "total": parkings.total,
            "page": parkings.page,
            "pages": parkings.pages,
            "has_next": parkings.has_next,
            "has_prev": parkings.has_prev,
            "parkings": [parking.to_dict() for parking in parkings],
        }

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@parking_bp.route("", methods=["POST"])
@parking_bp.arguments(ParkingSchema, location="json")
@role_required("admin")
def create_parking(args):
    """
    routes to create parkings
    """
    try:
        slots_num = args.get("slots_num")
        if slots_num is None or slots_num > 200 or slots_num < 10:
            raise APIError(
                "Parking must have at least 10 and at most 200 parking slots!",
                404,
            )

        if (
            Parking.query.filter_by(name=args.get("name")).first()
            or Parking.query.filter_by(
                name=args.get("name"), address=args.get("address")
            ).first()
        ):
            raise APIError(
                "Parking with that name & address is already exists!",
                409,
            )

        parking = Parking(
            name=args.get("name"),
            address=args.get("address"),
            pincode=args.get("pincode"),
            phone=args.get("phone"),
            lat=args.get("lat"),
            long=args.get("long"),
            hourly_fee=args.get("hourly_fee"),
            booking_fee=args.get("booking_fee"),
            slots_num=slots_num,
        )

        db.session.add(parking)
        db.session.flush()

        # creating slots
        db.session.add_all(
            [
                Slot(parking_id=parking.id, serial_id=f"PR{parking.id}SL{i}")
                for i in range(1, int(parking.slots_num) + 1)
            ]
        )
        db.session.commit()

        return {
            "message": "parking created successfully",
            "parking": parking.to_dict(),
        }, 200

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@parking_bp.route("", methods=["PUT"])
@parking_bp.arguments(ParkingSchema, location="json")
@role_required("admin")
def update_parking(args):
    """
    routes to update parkings
    """
    try:
        parking_id = args.get("id")
        if parking_id is None:
            raise APIError("Parking id must be provided!", 404)
        parking = Parking.query.get(int(parking_id))

        if not parking:
            raise APIError("Parking does not exist!", 404)

        parking.name = args.get("name")
        parking.address = args.get("address")
        parking.pincode = args.get("pincode")
        parking.phone = args.get("phone")
        parking.lat = args.get("lat")
        parking.long = args.get("long")
        parking.hourly_fee = args.get("hourly_fee")
        parking.booking_fee = args.get("booking_fee")

        db.session.commit()

        slots_num = args.get("slots_num")
        if slots_num is None or slots_num > 200 or slots_num < 10:
            return {
                "message": "parking update but slots numbers not updated as parking must have at least 10 and at most 200 slots!",
                "parking": parking.to_dict(),
            }, 201

        # handling slots number
        if slots_num > parking.slots_num:
            slots = parking.slots
            add_slots_num = int(slots_num) - len(slots)
            i = 1
            while add_slots_num > 0:
                serial_id = f"PR{parking.id}SL{i}"
                if not Slot.query.filter_by(serial_id=serial_id).first():
                    db.session.add(Slot(parking_id=parking.id, serial_id=serial_id))
                    add_slots_num -= 1
                i += 1

            parking.slots_num = slots_num
            db.session.commit()

        elif slots_num < parking.slots_num:
            if slots_num < 10:
                return {
                    "message": "parking update but slots numbers not updated as min slot required is 10!",
                    "parking": parking.to_dict(),
                }, 201

            to_dlt = []
            slots = parking.slots
            for slot in slots:
                if not slot.is_occupied:
                    to_dlt.append(slot)
                if len(to_dlt) == int(parking.slots_num - slots_num):
                    for sl in to_dlt:
                        db.session.delete(sl)
                    parking.slots_num = slots_num
                    db.session.commit()
                    return {
                        "message": "parking update successfully",
                        "parking": parking.to_dict(),
                    }, 201

            db.session.rollback()
            return {
                "message": "parking update successfully but slots can't be deleted as many of them occupied.",
                "parking": parking.to_dict(),
            }, 201

        db.session.commit()

        return {
            "message": "parking update successfully",
            "parking": parking.to_dict(),
        }, 201

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


# TODO: check update parking after booking slots


@parking_bp.route("", methods=["DELETE"])
@parking_bp.arguments(IdSchema, location="query")
@role_required("admin")
def delete_parking(args):
    """
    get parking by id
    """
    try:
        id = args.get("id")
        if not id:
            raise APIError("id must be given as query parameter!", 404)

        parking = Parking.query.get(id)

        if not parking:
            raise APIError("parking is not found!", status_code=404)

        # Only delete if no slots are occupied for this parking
        occupied_slots = Slot.query.filter_by(
            parking_id=parking.id, is_occupied=True
        ).all()
        if not occupied_slots:
            db.session.delete(parking)
            db.session.commit()
            return {"message": f"parking with id - {id} deleted successfully!"}, 200
        else:
            raise APIError(
                "parking's some slots are occupied, unable to delete!", status_code=404
            )

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@parking_bp.route("/slot")
@parking_bp.arguments(SlotQuerySchema, location="query")
def get_slot(args: dict):
    """
    query slots
    """
    try:
        page = args.get("page") or 1
        per_page = args.get("per_page") or 10

        if args.get("id"):
            slot = Slot.query.get(args.get("id"))
            if not slot:
                raise APIError("slot not found with this id!", 404)
            return slot.to_dict()

        if args.get("serial_id"):
            slot = Slot.query.filter_by(serial_id=args.get("serial_id")).first()
            if not slot:
                raise APIError("slot not found with this serial id!", 404)
            return slot.to_dict()

        if args.get("parking_id"):
            if args.get("occupied") is not None and args.get("occupied"):
                slots = Slot.query.filter_by(
                    parking_id=args.get("parking_id"), is_occupied=True
                ).paginate(page=page, per_page=per_page)
                return {
                    "total": slots.total,
                    "page": slots.page,
                    "pages": slots.pages,
                    "has_next": slots.has_next,
                    "has_prev": slots.has_prev,
                    "slots": [slot.to_dict() for slot in slots],
                }

            if args.get("occupied") is not None and not args.get("occupied"):
                slots = Slot.query.filter_by(
                    parking_id=args.get("parking_id"), is_occupied=False
                ).paginate(page=page, per_page=per_page)
                return {
                    "total": slots.total,
                    "page": slots.page,
                    "pages": slots.pages,
                    "has_next": slots.has_next,
                    "has_prev": slots.has_prev,
                    "slots": [slot.to_dict() for slot in slots],
                }

            slots = Slot.query.filter_by(parking_id=args.get("parking_id")).paginate(
                page=page, per_page=per_page
            )
            return {
                "total": slots.total,
                "page": slots.page,
                "pages": slots.pages,
                "has_next": slots.has_next,
                "has_prev": slots.has_prev,
                "slots": [slot.to_dict() for slot in slots],
            }

        raise APIError("invalid query!", 404)

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@parking_bp.route("/slot", methods=["DELETE"])
@parking_bp.arguments(SlotQuerySchema, location="query")
@role_required("admin")
def delete_slot(args):
    """
    Delete slot if it's free
    """
    try:
        serial_id = args.get("serial_id", None)
        if not serial_id:
            raise APIError("Serial id is required to delete a slot.", 404)

        slot = Slot.query.filter_by(serial_id=serial_id).first()
        if not slot:
            raise APIError("Invalid Serial id.", 404)

        parking = slot.parking
        parking.slots_num -= 1

        db.session.delete(slot)
        db.session.commit()

        return {"message": "Slot with serial number deleted successfully"}, 200

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")
