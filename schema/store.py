from ma import ma
from models.store import StoreModel
from schema.item import ItemSchema


class StoreSchema(ma.Schema):
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel
        dump_only = ('id')
        include_fk = True
