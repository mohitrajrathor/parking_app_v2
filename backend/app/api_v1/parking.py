# parking related routes

# imports
from flask_smorest import Blueprint, abort
from ..schema import QuerySchema, ParkingSchema, ParkingResponseSchema
from ..extensions import db
from ..models import Parking, Slot
from ..exceptions import APIError
from flask import current_app


parking_bp = Blueprint(
    "parking", __name__, url_prefix="/parking", description="parking related routes"
)


@parking_bp.route("", methods=["GET"])
@parking_bp.arguments(QuerySchema, location="query")
@parking_bp.response(200, ParkingResponseSchema)
def get_parking(args):
    """
    query parkings
    """
    try:
        if args.get("id"):
            parking = Parking.query.get(args.get("id"))
            return parking.to_dict()

        if args.get("query"):
            parkings = Parking.query.filter(
                Parking.name.ilike(f"%{args.get('query')}%")
            ).all()

            return {
                "total": len(parkings),
                "parkings": [parking.to_dict() for parking in parkings],
            }, 200

        if args.get("lat") and args.get("long"):
            # TODO: calcualte parking distance and then return closest parkings
            ...

        return {"message": "route is working"}, 200

    except APIError as e:
        current_app.logger.error(e.message)
        return abort(e.status_code, message=str(e), additional_data=e.extra)

    except Exception as e:
        current_app.logger.error(e)
        return abort(500, message="Internal Server Error.")


@parking_bp.route("", methods=["POST"])
@parking_bp.arguments(ParkingSchema, location="json")
def create_parking(args):
    """
    routes to get parkings
    """
    try:

        if Parking.query.filter_by(name=args["name"], address=args["address"]).first():
            raise APIError("Parking with that name & address is already exists!", 404)

        parking = Parking(
            name=args["name"],
            address=args["address"],
            pincode=args["pincode"],
            phone=args["phone"],
            lat=args["lat"],
            long=args["long"],
            fee=args["fee"],
            slots_num=args["slots_num"],
        )

        db.session.flush(parking)

        # creating slots
        db.session.add_all(
            [
                Slot(parking_id=parking.id, serial_id=f"PR{parking.id}SL{i}")
                for i in range(1, parking.slots_num + 1)
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
def update_parking(args):
    """
    routes to get parkings
    """
    try:

        if Parking.query.filter_by(name=args["name"], address=args["address"]).first():
            raise APIError("Parking with that name & address is already exists!", 404)

        parking = Parking(
            name=args["name"],
            address=args["address"],
            pincode=args["pincode"],
            phone=args["phone"],
            lat=args["lat"],
            long=args["long"],
            fee=args["fee"],
            slots_num=args["slots_num"],
        )

        db.session.flush(parking)

        # creating slots
        db.session.add_all(
            [
                Slot(parking_id=parking.id, serial_id=f"PR{parking.id}SL{i}")
                for i in range(1, parking.slots_num + 1)
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
