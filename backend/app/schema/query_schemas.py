# to manage query related schemaas

# imports
from marshmallow import Schema, fields


class IdSchema(Schema):
    id = fields.Integer()


class QuerySchema(IdSchema):
    query = fields.Str()
    page = fields.Integer()
    lat = fields.Float()
    long = fields.Float()
    page = fields.Integer()
    per_page = fields.Integer()


class SlotQuerySchema(QuerySchema):
    parking_id = fields.Str()
    serial_id = fields.Str()
    occupied = fields.Boolean()
