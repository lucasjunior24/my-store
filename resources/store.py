import uuid
from flask.views import MethodView 
from flask_smorest import abort, Blueprint

from schemas import StoreSchema


blp = Blueprint("store", __name__, description="Operations on Store")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")


    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found")

    
@blp.route('/store')
class StoreList(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store["name"] == store_data["name"]:
                abort(404, message="Store already exists.")
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        
        return store, 201
    

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # return "Hello world"
        return stores.values()
