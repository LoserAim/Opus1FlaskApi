from src.controllers.users_controller import UserApi, UsersApi


def initialize_routes(api):
    api.add_resource(UserApi, '/api/users/<int:user_id>')
    api.add_resource(UsersApi, '/api/users')
