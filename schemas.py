from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(load_only=True, required=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)



class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainStoreSchema(), dump_only=True))
