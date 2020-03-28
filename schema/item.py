from ma import ma
from models.item import ItemModel


class ItemSchema(ma.Schema):
    class Meta:
        model = ItemModel
        load_only = ('store',)  # store_id and store almost are almost identical.
        dump_only = ('id')
        include_fk = True
