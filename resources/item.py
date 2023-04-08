from flask import request
import uuid
from flask.views import MethodView 
from flask_smorest import abort, Blueprint
from db import items, stores


blp = Blueprint("Itens", __name__, description="Operations on Item")

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")


    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found")

    def put(item_id):
        item_data = request.get_json()
        try:
            item = items[item_id]
            item != item_data
            return item
        except KeyError:
            abort(404, message="Item not found")

    
@blp.route('/item')
class ItemList(MethodView):
    def post(self):
        item_data = request.get_json()
        print(item_data)
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found.")
        
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item, 201
    

    def get(self):
        return {"items": list(items.values())}