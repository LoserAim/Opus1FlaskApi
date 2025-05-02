from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, marshal, abort, fields, marshal_with

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}, email = {self.email})"

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
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201


class UserApi(Resource):
    @marshal_with(userFields)
    def get(self, id: int):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, description={"message": "User not found"})
        return user

    @marshal_with(userFields)
    def patch(self, id: int):

        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, description={"message": "User not found"})

        user.name = args["name"]
        user.email = args["email"]
        db.session.commit()
        return user

    @marshal_with(userFields)
    def delete(self, id: int):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, description={"message": "User not found"})
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 204



api.add_resource(UsersApi, '/api/users')
api.add_resource(UserApi, '/api/users/<int:id>')

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
