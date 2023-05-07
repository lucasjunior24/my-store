
from db import db
from typing import cast
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

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

    @classmethod
    def validate_user(self, user_data):
        user = self.query.filter(
            self.username == user_data["username"]
        ).first()
        user = cast(UserModel, user)
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return access_token
        return ''
        