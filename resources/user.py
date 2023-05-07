from flask.views import MethodView 
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token
from models import UserModel
from schemas import UserSchema


blp = Blueprint("Users", "users", description="Operations on User")

@blp.route('/register')
class UserRegister(MethodView):    
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            user.save_user()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        return {"message": "User created successfully!"}, 201
    

@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        user.delete_user()
        return {"message": "User deleted."}
    

@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        access_token = UserModel.validate_user(user_data)
        return {"access_token": access_token} if access_token else abort(401, message="Invalid credentials.")


