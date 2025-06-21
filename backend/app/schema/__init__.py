# all schemas

# imports
from .auth_schemas import (
    UserLoginSchema,
    AdminLoginSchema,
    TokenSchema,
    UserSignupSchema,
)
from .parkings import ParkingSchema, SlotSchema, ParkingResponseSchema
from marshmallow import Schema, fields

__all__ = [
    "AdminLoginSchema",
    "UserLoginSchema",
    "TokenSchema",
    "UserSignupSchema",
    "ParkingSchema",
    "SlotSchema",
    "ParkingResponseSchema",
]


class QuerySchema(Schema):
    id = fields.Integer()
    query = fields.Str()
    page = fields.Integer()
    lat = fields.Float()
    long = fields.Float()
