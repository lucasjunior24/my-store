from typing import cast
from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), unique=False, nullable=False)

    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")


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
        item = cast(ItemModel, item)
        return item
    
    @classmethod
    def get(cls, id: int):
        item = cls.query.get(id)
        item = cast(ItemModel, item)
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