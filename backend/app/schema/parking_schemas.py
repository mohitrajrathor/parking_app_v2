# to manage parkings related schemas

# imports
from marshmallow import Schema, fields


class SlotSchema(Schema):
    id = fields.Integer()
    parking_id = fields.Integer()
    serial_id = fields.Str()
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
    create_time = fields.Str()


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    email = fields.Str()


class ReviewSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    parking_id = fields.Integer()
    feedback = fields.Str()
    rating = fields.Integer()
    create_at = fields.Str()
    # user contain dict having id, name, email
    user = fields.Nested(UserSchema)

class ParkingWithSlothSchema(ParkingSchema):
    slots = fields.List(fields.Nested(SlotSchema))
    booked = fields.Integer()
    reviews_count = fields.Integer()
    reviews = fields.List(fields.Nested(ReviewSchema))


class ParkingResponseSchema(ParkingSchema):
    parkings = fields.List(fields.Nested(ParkingWithSlothSchema))
    total = fields.Integer()
    page = fields.Integer()
    pages = fields.Integer()
    has_next = fields.Boolean()
    has_prev = fields.Boolean()
