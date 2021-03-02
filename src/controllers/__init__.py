from src.controllers.auth_controller import auth
from src.controllers.teams_controller import teams
from src.controllers.users_controller import users

registerable_controllers = [
    auth,
    teams,
    users
]
