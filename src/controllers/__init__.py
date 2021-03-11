from src.controllers.auth_controller import auth
from src.controllers.pokemon_controller import pokemon
from src.controllers.moves_controller import moves
from src.controllers.teams_controller import teams
from src.controllers.users_controller import users

registerable_controllers = [
    auth,
    pokemon,
    moves,
    teams,
    users
]
