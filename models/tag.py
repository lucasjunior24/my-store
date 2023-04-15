from typing import cast
from db import db


class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")


    def json(self):
        return {
                    "site_id": self.site_id,
                    "url": self.url,
                    "name": self.name,
                    "hoteis": [hotel.json() for hotel in self.hoteis]
                }
    

    @classmethod
    def find_tag(cls, id: int):
        tag = cls.query.get_or_404(id)
        tag = cast(TagModel, tag)
        return tag
    

    @classmethod
    def get(cls, id: int):
        tag = cls.query.get(id)
        tag = cast(TagModel, tag)
        return tag
    

    def save_tag(self):
        db.session.add(self)
        db.session.commit()


    def update_tag(self, name):
        self.name = name


    def delete_tag(self):
        db.session.delete(self)
        db.session.commit()