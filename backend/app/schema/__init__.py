# all schemas

# imports
from .auth_schemas import (
    UserLoginSchema,
    AdminLoginSchema,
    TokenSchema,
    UserSignupSchema,
)
from .parking_schemas import (
    ParkingSchema,
    SlotSchema,
    ParkingResponseSchema,
    ParkingWithSlothSchema,
)

from .query_schemas import IdSchema, QuerySchema, SlotQuerySchema


__all__ = [
    "AdminLoginSchema",
    "UserLoginSchema",
    "TokenSchema",
    "UserSignupSchema",
    "ParkingSchema",
    "SlotSchema",
    "ParkingResponseSchema",
    "ParkingWithSlothSchema",
    "SlotQuerySchema",
    "IdSchema",
    "QuerySchema",
]
