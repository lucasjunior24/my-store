
from db import db
from typing import cast

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
    
    def json(self):
        return {
                    "id": self.id,
                    "username": self.username,
                }
    

    @classmethod
    def find_user(cls, id: int):
        user = cls.query.get_or_404(id)
        user = cast(UserModel, user)
        return user
    
    @classmethod
    def get(cls, id: int):
        user = cls.query.get(id)
        user = cast(UserModel, user)
        return user
    

    def save_user(self):
        db.session.add(self)
        db.session.commit()


    def update_user(self, name):
        self.username = name


    def delete_user(self):
        db.session.delete(self)
        db.session.commit()