from typing import cast
from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")

    def json(self):
        return {
            "site_id": self.site_id,
            "url": self.url,
            "name": self.name,
            "hoteis": [hotel.json() for hotel in self.hoteis]
        }
    

    @classmethod
    def find_store(cls, id: int):
        store = cls.query.get_or_404(id)
        store = cast(StoreModel, store)
        return store
    

    @classmethod
    def get(cls, id: int):
        store = cls.query.get(id)
        store = cast(StoreModel, store)
        return store
    

    def save_store(self):
        db.session.add(self)
        db.session.commit()


    def update_store(self, name):
        self.name = name


    def delete_store(self):
        # [hotel.delete_hotel() for hotel in self.hoteis]
        db.session.delete(self)
        db.session.commit()