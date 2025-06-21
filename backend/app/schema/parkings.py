# to manage parkings related schemas

# imports
from marshmallow import Schema, fields, validates, ValidationError


class SlotSchema(Schema):
    id = fields.Integer()
    parking_id = fields.Integer()
    serial_id = fields.Integer()
    is_occupied = fields.Boolean()


class ParkingSchema(Schema):
    id = fields.Integer()
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    pincode = fields.Str(required=True)
    phone = fields.Str(required=True)
    lat = fields.Float(required=True)
    long = fields.Float(required=True)
    fee = fields.Float(required=True)
    slots_num = fields.Float(required=True)


class ParkingResponseSchema(ParkingSchema):
    slots = fields.List(fields.Nested(ParkingSchema))
