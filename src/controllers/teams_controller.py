from flask import abort, Blueprint, jsonify

from src.main import db
from src.models.User import User
from src.models.Team import Team
from src.models.Pokemon import Pokemon
from src.schemas.TeamSchema import team_schema
from src.schemas.PokemonSchema import pokemon_schema

teams = Blueprint("teams", __name__, url_prefix="/teams")


@teams.route("/<int:team_id>", methods=["GET"])
def get_team(team_id):

    team = db.session.query(Team, Pokemon)\
        .join(Pokemon, Team.id == Pokemon.team_id)\
        .order_by(Pokemon.team_index)\
        .filter(Team.id == team_id).all()

    print(team)
    return jsonify(team_schema.dump(team[0][0]), pokemon_schema.dump(team[0][1]))
