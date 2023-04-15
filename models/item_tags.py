from typing import cast
from db import db


class ItemTagsModel(db.Model):
    __tablename__ = 'items_tags'

    id = db.Column(db.Integer, primary_key=True)
    items_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    tags_id = db.Column(db.Integer, db.ForeignKey('tags.id'))


    def json(self):
        return {
            "site_id": self.site_id,
            "url": self.url,
            "name": self.name,
            "hoteis": [hotel.json() for hotel in self.hoteis]
        }
    
    @classmethod
    def find_item(cls, id: int):
        item = cls.query.get_or_404(id)
        item = cast(ItemTagsModel, item)
        return item
    
    @classmethod
    def get(cls, id: int):
        item = cls.query.get(id)
        item = cast(ItemTagsModel, item)
        return item
    
    
    def save_item(self):
        db.session.add(self)
        db.session.commit()


    def update_item(self, price: str, name: str):
        self.price = price
        self.name = name


    def delete_item(self):
        # [hotel.delete_hotel() for hotel in self.hoteis]
        db.session.delete(self)
        db.session.commit()