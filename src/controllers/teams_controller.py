from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from src.forms import CreateTeamForm, DeleteTeamForm, EditTeamForm
from src.main import db
from src.models.Team import Team
from src.models.TeamsPokemon import Teams_Pokemon
from src.models.PokemonMoves import Pokemon_Moves
import src.schemas.MoveSchema                                           # noqa: F401
import src.schemas.PokemonSchema                                        # noqa: F401
from src.schemas.TeamSchema import team_schema, teams_schema
import src.schemas.TeamsPokemonSchema                                   # noqa: F401
from src.schemas.PokemonMovesSchema import pokemon_moves_schema

teams = Blueprint("teams", __name__)


@teams.route("/my-teams", methods=["GET"])
@login_required
def get_users_teams():
    team_list = Team.query.filter_by(owner_id=current_user.id).all()

    team_list_dict = teams_schema.dump(team_list)
    for team in team_list_dict:
        indices = [pokemon["team_index"] for pokemon in team["team_pokemon"]]
        for i in range(6):
            if i + 1 not in indices:
                team["team_pokemon"].insert(i, None)

    return render_template("team_list.html", teams=team_list_dict, type="personal")


@teams.route("/teams", methods=["GET"])
def get_public_teams():
    team_list = Team.query.filter_by(is_private=False).all()

    team_list_dict = teams_schema.dump(team_list)
    for team in team_list_dict:
        indices = [pokemon["team_index"] for pokemon in team["team_pokemon"]]
        for i in range(6):
            if i + 1 not in indices:
                team["team_pokemon"].insert(i, None)

    return render_template("team_list.html", teams=team_list, type="public")


@teams.route("/teams/create", methods=["GET", "POST"])
@login_required
def create_team():
    form = CreateTeamForm()
    if form.validate_on_submit():
        team = Team()
        team.name = form.team_name.data
        team.description = form.description.data
        team.is_private = form.is_private.data

        current_user.teams.append(team)
        db.session.commit()

        return redirect(url_for("teams.get_team", team_id=team.id))

    return render_template("team_create.html", form=form)


@teams.route("/teams/<int:team_id>", methods=["GET"])
def get_team(team_id):
    form = DeleteTeamForm()
    team = Team.query.get(team_id)

    # Need to query pokemon moves separately
    query_moves = db.session.query(Teams_Pokemon, Pokemon_Moves)\
        .join(Pokemon_Moves, Teams_Pokemon.id == Pokemon_Moves.team_pokemon_id)\
        .order_by(Teams_Pokemon.team_index, Pokemon_Moves.pokemon_move_index)\
        .filter(Teams_Pokemon.team_id == team_id)\
        .all()

    # Fill any empty pokemon slots in team with None
    # Needs to be done in dict otherwise SQLAlchemy will try to insert None objects into the database
    team_dict = team_schema.dump(team)
    indices = [pokemon.team_index for pokemon in team.team_pokemon]
    for i in range(6):
        if i + 1 not in indices:
            team_dict["team_pokemon"].insert(i, None)

    # Format query results to group moves into move sets by pokemon pokeapi.id
    ids = {q[1].pokeapi_id for q in query_moves}
    move_sets = [[q[1] for q in query_moves if q[1].pokeapi_id == id] for id in ids]

    # Fill any empty move slots with None, again needs to be done as a dict
    move_sets_dict = [pokemon_moves_schema.dump(move_set) for move_set in move_sets]
    for move_set in move_sets:
        indices = [move.pokemon_move_index for move in move_set]
        for i in range(4):
            if i + 1 not in indices:
                move_sets_dict.insert(i, None)

    # team_pokemon_ids = []
    # for move_set in move_sets:
    #     for move in move_set:
    #         team_pokemon_ids.append(move.team_pokemon_id)
    # team_pokemon_ids = set(team_pokemon_ids)

    # Fill move_sets_dict with None for empty pokemon slots or if pokemon has no moves assigned to it
    team_pokemon_ids = {move.team_pokemon_id for move_set in move_sets for move in move_set}
    for i in range(6):
        if team_dict["team_pokemon"][i] is None or team_dict["team_pokemon"][i]["id"] not in team_pokemon_ids:
            move_sets_dict.insert(i, None)

    return render_template("team_view.html", form=form, team=team_dict, move_sets=move_sets_dict)


@teams.route("/teams/<int:team_id>/edit", methods=["GET", "POST"])
@login_required
def edit_team_details(team_id):

    team = Team.query.filter_by(id=team_id)
    if current_user.id == team[0].owner_id:
        form = EditTeamForm()
        if form.validate_on_submit():
            data = {}
            if form.team_name.data:
                data["name"] = form.team_name.data
            if form.description.data:
                data["description"] = form.description.data
            data["is_private"] = form.is_private.data

            fields = team_schema.load(data, partial=True)

            team.update(fields)
            db.session.commit()

            flash("Team details updated successfully.")
            return redirect(url_for("teams.get_team", team_id=team_id))

        form.team_name.data = team[0].name
        form.description.data = team[0].description
        form.is_private.data = team[0].is_private

        return render_template("team_edit.html", form=form, team_id=team_id)
    else:
        flash("You do not have permission to edit this team.")
        return redirect(url_for("teams.get_team", team_id=team_id))


@teams.route("/teams/<int:team_id>/delete", methods=["POST"])
@login_required
def delete_team(team_id):
    team = Team.query.get(team_id)
    if current_user.id == team.owner_id:
        form = DeleteTeamForm()
        if form.validate_on_submit():
            team = Team.query.get(team_id)

            db.session.delete(team)
            db.session.commit()

            flash("Team successfully deleted.")

            return redirect(url_for("teams.get_users_teams"))
    else:
        flash("You do not have permission to delete this team.")
        return redirect(url_for("team.get_team", team_id=team.id))
