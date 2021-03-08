from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from src.forms import DeleteTeamForm
from src.main import db
# from src.models.User import User
from src.models.Team import Team
# from src.models.TeamsPokemon import Teams_Pokemon
# from src.models.Pokemon import Pokemon
# from src.models.PokemonMoves import Pokemon_Moves
# from src.schemas.TeamSchema import team_schema
# from src.schemas.TeamsPokemonSchema import teams_pokemon_schema, teams_pokemon_many_schema
# from src.schemas.PokemonSchema import pokemon_schema, pokemon_many_schema
# from src.schemas.PokemonMovesSchema import pokemon_move_schema, pokemon_moves_schema
# from src.schemas.MoveSchema import move_schema

teams = Blueprint("teams", __name__)


@teams.route("/my-teams", methods=["GET"])
@login_required
def get_users_teams():
    teams = Team.query.filter_by(owner_id=current_user.id).all()
    return render_template("team_list.html", teams=teams, type="personal")


@teams.route("/teams", methods=["GET"])
def get_public_teams():
    teams = Team.query.filter_by(is_private=False).all()
    return render_template("team_list.html", teams=teams, type="public")


@teams.route("/teams/create", methods=["GET", "POST"])
@login_required
def create_team():
    pass


@teams.route("/teams/<int:team_id>", methods=["GET"])
def get_team(team_id):
    form = DeleteTeamForm()
    return render_template("team_view.html", form=form)


@teams.route("/teams/<int:team_id>/edit", methods=["GET", "POST"])
@login_required
def edit_team_details(team_id):
    pass


@teams.route("/teams/<int:team_id>/delete", methods=["POST"])
@login_required
def delete_team(team_id):
    form = DeleteTeamForm()
    if form.validate_on_submit():
        team = Team.query.get(team_id)
        if current_user.id == team.owner_id:

            db.session.delete(team)
            db.session.commit()

            flash("Team successfully deleted.")

            return redirect(url_for("teams.get_users_teams"))

        else:
            flash("You do not have permission to delete this team.")
            return redirect(url_for("team.get_team", team_id))

    # team = Team.query.get(team_id)

    # return jsonify(team_schema.dump(team))

    # query = db.session.query(Teams_Pokemon, Pokemon_Moves)\
    #     .join(Pokemon_Moves, Teams_Pokemon.id == Pokemon_Moves.team_pokemon_id)\
    #     .order_by(Teams_Pokemon.team_index, Pokemon_Moves.pokemon_move_index)\
    #     .filter(Teams_Pokemon.team_id == team_id)\
    #     .all()

    # ids = {q[1].pokeapi_id for q in query}
    # moves = [[q[1] for q in query if q[1].pokeapi_id == id] for id in ids]

    # print(moves)
    # return jsonify([pokemon_moves_schema.dump(move) for move in moves])
