# module to store user schemas 


# imports
from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    email = fields.Email()
    