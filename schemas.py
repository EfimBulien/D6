from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    description = fields.String(required=True)
    price = fields.Float(required=True)
    category = fields.String(required=True)
    