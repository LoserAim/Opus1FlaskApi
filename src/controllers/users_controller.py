from flask_restful import Resource, reqparse, abort, fields, marshal_with
from src.models.user_model import User
from src import db

user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="name cannot be blank")
user_args.add_argument("email", type=str, required=True, help="email cannot be blank")

userFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String
}

class UsersApi(Resource):

    @marshal_with(userFields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = User(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        users = User.query.all()
        return users, 201


class UserApi(Resource):
    @marshal_with(userFields)
    def get(self, user_id: int):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, description={"message": "User not found"})
        return user

    @marshal_with(userFields)
    def patch(self, user_id: int):

        args = user_args.parse_args()
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, description={"message": "User not found"})

        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user

    @marshal_with(userFields)
    def delete(self, user_id: int):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404, description={"message": "User not found"})
        db.session.delete(user)
        db.session.commit()
        users = User.query.all()
        return users, 204