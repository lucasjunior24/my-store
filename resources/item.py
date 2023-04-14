from flask.views import MethodView 
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from typing import cast

from models import ItemModel
from db import db
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("Itens", __name__, description="Operations on Item")

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.find_item(item_id)
        return item


    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("deleting an item is not implemented")


    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        item = cast(ItemModel, item)
        if item:
            item.update_site(**item_data)
        else:
            item = ItemModel(id=item_id, **item_data)
        item.save_item()
        return item
    
@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            item.save_item()
        except SQLAlchemyError:
            abort(500, message="An error occurred whilte inserting the item.")

        return item, 201