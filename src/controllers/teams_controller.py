from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from src.forms import CreateTeamForm, DeleteTeamForm, EditTeamForm
from src.main import db
from src.models.Team import Team
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
    """
    Returns the personal team list page for a logged in user.
    """

    team_list = Team.query.filter_by(owner_id=current_user.id).all()
    team_list = Team.sort_team_pokemon(team_list)
    team_list_dict = teams_schema.dump(team_list)
    team_list_dict = Team.fill_empty_team_slots(team_list_dict)
    return render_template("team_list.html", teams=team_list_dict, type="personal")


@teams.route("/teams", methods=["GET"])
def get_public_teams():
    """
    Returns the public team list page.
    """

    team_list = Team.query.filter_by(is_private=False).all()
    team_list = Team.sort_team_pokemon(team_list)
    team_list_dict = teams_schema.dump(team_list)
    team_list_dict = Team.fill_empty_team_slots(team_list_dict)
    return render_template("team_list.html", teams=team_list_dict, type="public")


@teams.route("/teams/create", methods=["GET", "POST"])
@login_required
def create_team():
    """
    GET returns the template for the create team page, when the form is submitted the data is
    sent back to the endpoint using POST which creates the team.
    """

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
    """
    Returns the team view page for a team, to get the template displaying correctly the
    pokemon and move data needs to be filled with None objects for empty slots
    """

    form = DeleteTeamForm()
    team = Team.query.get(team_id)
    team.team_pokemon.sort(key=lambda x: x.team_index)

    # Get the move set for each pokemon
    move_sets = []
    for pokemon in team.team_pokemon:
        move_sets.append(Pokemon_Moves.query.filter_by(team_pokemon_id=pokemon.id).order_by(Pokemon_Moves.pokemon_move_index).all())

    # Fill any empty pokemon slots in team with None
    # Needs to be done in dict otherwise SQLAlchemy will try to insert None objects into the database
    team_dict = team_schema.dump(team)
    indices = [pokemon.team_index for pokemon in team.team_pokemon]
    for i in range(6):
        if i + 1 not in indices:
            team_dict["team_pokemon"].insert(i, None)

    # Fill any empty move slots within each move set with None, again needs to be done as a dict
    move_sets_dict = [pokemon_moves_schema.dump(move_set) for move_set in move_sets]
    for move_set in move_sets_dict:
        indices = [move["pokemon_move_index"] for move in move_set]
        for i in range(4):
            if i + 1 not in indices:
                move_set.insert(i, None)

    # Fill move_sets_dict with None for empty pokemon slots or if pokemon has no moves assigned to it
    team_pokemon_ids = [pokemon.team_index for pokemon in team.team_pokemon]
    for i in range(6):
        if i + 1 not in team_pokemon_ids:
            move_sets_dict.insert(i, None)

    return render_template("team_view.html", form=form, team=team_dict, team_id=team_id, move_sets=move_sets_dict)


@teams.route("/teams/<int:team_id>/edit", methods=["GET", "POST"])
def edit_team_details(team_id):
    """
    GET returns the template for the edit team page, when the form is submitted the data is
    sent back to the endpoint using POST which updates the team data.
    """

    team = Team.query.filter_by(id=team_id)

    # Check is to prevent users from accessing the endpoint by manually entering the url if it's not their team
    if current_user.is_authenticated and current_user.id == team[0].owner_id:
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

        # Prepopulate the form with existing data
        form.team_name.data = team[0].name
        form.description.data = team[0].description
        form.is_private.data = team[0].is_private

        return render_template("team_edit.html", form=form, team_id=team_id)
    else:
        flash("You do not have permission to edit this team.")
        return redirect(url_for("teams.get_public_teams"))


@teams.route("/teams/<int:team_id>/delete", methods=["POST"])
def delete_team(team_id):
    """
    Deletes the team from the database with a cascading effect on all child entries.
    """

    team = Team.query.get(team_id)

    # Check is to prevent users from accessing the endpoint by manually entering the url if it's not their team
    if current_user.is_authenticated and current_user.id == team.owner_id:
        form = DeleteTeamForm()
        if form.validate_on_submit():
            team = Team.query.get(team_id)

            db.session.delete(team)
            db.session.commit()

            flash("Team successfully deleted.")

            return redirect(url_for("teams.get_users_teams"))
    else:
        flash("You do not have permission to delete this team.")
        return redirect(url_for("teams.get_public_teams"))
