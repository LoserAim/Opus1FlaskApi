from src.controllers.users_controller import UserApi, UsersApi


def initialize_routes(api):
    api.add_resource(UserApi, '/api/user/<int:id>')
    api.add_resource(UsersApi, '/api/users')
