import uuid
from flask.views import MethodView 
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import StoreModel, TagModel
from schemas import TagSchema


blp = Blueprint("Tags", "tags", description="Operations on Tag")

@blp.route('/store/<int:store_id>/tag')
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.find_store(store_id)
        return store.tags.all()

    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            tag.save_tag()
        except IntegrityError:
            abort(400, message="A tag with name already exists.")
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag, 201

    # def delete(self, store_id):
    #     store = StoreModel.find_store(store_id)
    #     store.delete_store()
    #     return {"message": "Store deleted."}

    
@blp.route('/tag/<string:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.find_tag(tag_id)
        return tag
    
