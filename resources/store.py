from flask import request
import uuid
from flask.views import MethodView 
from flask_smorest import abort, Blueprint
from db import stores
from schemas import StoreSchema


blp = Blueprint("store", __name__, description="Operations on Store")

@blp.route('/store/<string:store_id>')
class Store(MethodView):
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
    def post(self, store_data):
        for store in stores.values():
            if store["name"] == store_data["name"]:
                abort(404, message="Store already exists.")
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        
        return store, 201
    

    def get(self):
        # return "Hello world"
        return {"stores": list(stores.values())}
