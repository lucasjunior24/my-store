from flask.views import MethodView 
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import StoreModel, TagModel, ItemModel
from schemas import TagSchema, TagAndItemSchema


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
    

@blp.route('/item/<int:item_id>/tag/<int:tag_id>')
class LinkTagsToItems(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.find_item(item_id)
        tag = TagModel.find_tag(tag_id)

        item.tags.append(tag)
        try:
            item.save_item()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return tag
    
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.find_item(item_id)
        tag = TagModel.find_tag(tag_id)

        item.tags.remove(tag)
        try:
            item.save_item()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": "Item removed from Tag", "item": item, "tag": tag}


    
@blp.route('/tag/<string:tag_id>')
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.find_tag(tag_id)
        return tag
    
    
    @blp.response(
        202, 
        description="Deletes a tag if no items is tagged with it.",
        example={"message": "Tag deleted."}
    )
    @blp.response(404, description="Tag not found.")
    @blp.response(200, TagSchema)
    def delete(self, tag_id):
        tag = TagModel.find_tag(tag_id)
        if not tag.items:
            tag.delete_tag()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again."
        )