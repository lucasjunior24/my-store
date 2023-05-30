from flask.views import MethodView 
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("Itens", __name__, description="Operations on Item")

@blp.route('/item/<int:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.find_item(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        item = ItemModel.find_item(item_id)
        item.delete_item()
        return {"message": "Item deleted."}

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.get(item_id)
        if item:
            item.update_item(**item_data)
        else:
            item = ItemModel(id=item_id, **item_data)
        item.save_item()
        return item
    
    
@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            item.save_item()
        except SQLAlchemyError:
            abort(500, message="An error occurred whilte inserting the item.")

        return item, 201