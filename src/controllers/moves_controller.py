from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from src.forms import ConfirmForm, RemoveMoveForm
from src.main import db
from src.models.Move import Move
from src.models.Pokemon import Pokemon
from src.models.PokemonMoves import Pokemon_Moves
from src.models.Team import Team
from src.schemas.PokemonMovesSchema import pokemon_move_schema


moves = Blueprint("moves", __name__)


@moves.route("/teams/<int:team_id>/<int:team_index>/<int:pokemon_move_index>", methods=["GET"])
def view_pokemon_move(team_id, team_index, pokemon_move_index):
    """
    Returns the move view page for a move known by a pokemon on a team.
    """

    form = RemoveMoveForm()
    team_pokemon = Teams_Pokemon.query.get((team_id, team_index))
    move = Pokemon_Moves.query.get((team_pokemon.id, team_pokemon.pokeapi_id, pokemon_move_index))

    # If move slot is empty skip the move view page and go straight to the move list page to select a move
    if not move:
        return redirect(url_for("moves.get_pokemon_move_list", team_id=team_id,
                                team_index=team_index, pokemon_move_index=pokemon_move_index))

    api_data = Move.get_move_data(move.move_id)
    return render_template("move_view.html", form=form, data=api_data, team_pokemon=team_pokemon, team_id=team_id,
                           team_index=team_index, pokemon_move_index=pokemon_move_index, type="team")


@moves.route("/teams/<int:team_id>/<int:team_index>/<int:pokemon_move_index>/select", methods=["GET"])
@login_required
def get_pokemon_move_list(team_id, team_index, pokemon_move_index):
    """
    Returns the move list page for a pokemon on a team.
    """

    team_pokemon = Teams_Pokemon.query.get((team_id, team_index))

    # Get current move as the back button on the template will need a different url if the current move is empty
    current_move = Pokemon_Moves.query.filter_by(team_pokemon_id=team_pokemon.id, pokemon_move_index=pokemon_move_index).first()
    
    # Check is to prevent users from accessing the endpoint by manually entering the url if it's not their team
    if current_user.id == team_pokemon.team.owner_id:
       
       # Get the Pokemons currently learned moves so that they can be excluded from the move list
        move_set = Pokemon_Moves.query.filter_by(team_pokemon_id=team_pokemon.id).order_by(Pokemon_Moves.pokemon_move_index).all()
        move_list = Move.get_move_list(Pokemon.get_pokemon_data(team_pokemon.pokeapi_id), move_set)
        return render_template("move_select.html", move_list=move_list, team_pokemon=team_pokemon, current_move=current_move,
                               team_id=team_id, team_index=team_index, pokemon_move_index=pokemon_move_index)
    else:
        flash("You do not have permission to change this move.")
        return redirect(url_for("teams.get_public_teams"))


@moves.route("/teams/<int:team_id>/<int:team_index>/<int:pokemon_move_index>/select/<int:move_id>", methods=["GET"])
@login_required
def view_selected_pokemon_move(team_id, team_index, pokemon_move_index, move_id):
    """
    Returns the move view page for the move selected on the previous move list page.
    """

    team_pokemon = Teams_Pokemon.query.get((team_id, team_index))
    # Check is to prevent users from accessing the endpoint by manually entering the url if it's not their team
    if current_user.id == team_pokemon.team.owner_id:
        form = ConfirmForm()
        api_data = Move.get_move_data(move_id)
        return render_template("move_view.html", form=form, data=api_data, team_pokemon=team_pokemon, team_id=team_id, team_index=team_index,
                               pokemon_move_index=pokemon_move_index, move_id=move_id, type="team-selected")
    else:
        flash("You do not have permission to change this move.")
        return redirect(url_for("teams.get_public_teams"))


@moves.route("/teams/<int:team_id>/<int:team_index>/<int:pokemon_move_index>/edit/<int:move_id>", methods=["POST"])
@login_required
def edit_pokemon_move_slot(team_id, team_index, pokemon_move_index, move_id):
    """
    Adds a new move to a pokemon or updates an existing move and returns the user to the pokemon view page.
    """

    team_pokemon = Teams_Pokemon.query.get((team_id, team_index))
    # Check is to prevent users from accessing the endpoint by manually entering the url if it's not their team
    if current_user.id == team_pokemon.team.owner_id:
        form = ConfirmForm()
        if form.validate_on_submit():

            # Create new entry if move not already in database
            move = Move.query.get(move_id)
            if not move:
                move_api_data = Move.get_move_data(move_id)
                move = Move()
                move.move_id = move_id
                move.move_name = move_api_data["name"]
                db.session.add(move)
                db.session.commit()

            # Create new entry if there is no existing pokemon_moves for this team_pokemon id, pokeapi id and pokemon move index,
            # otherwise update the existing entry
            pokemon_move = Pokemon_Moves.query.filter_by(team_pokemon_id=team_pokemon.id, pokeapi_id=team_pokemon.pokeapi_id,
                                                         pokemon_move_index=pokemon_move_index).first()
            if not pokemon_move:
                new_pokemon_move = Pokemon_Moves()
                new_pokemon_move.team_pokemon_id = team_pokemon.id
                new_pokemon_move.pokeapi_id = team_pokemon.pokeapi_id
                new_pokemon_move.pokemon_move_index = pokemon_move_index
                new_pokemon_move.move_id = move_id
                team_pokemon.pokemon_moves.append(new_pokemon_move)
            else:
                pokemon_moves = Pokemon_Moves.query.filter_by(team_pokemon_id=team_pokemon.id, pokeapi_id=team_pokemon.pokeapi_id,
                                                              pokemon_move_index=pokemon_move_index)
                data = {
                    "team_pokemon_id": team_pokemon.id,
                    "pokeapi_id": team_pokemon.pokeapi_id,
                    "pokemon_move_index": pokemon_move_index,
                    "move_id": move_id
                }

                pokemon_moves.update(pokemon_move_schema.load(data, partial=True))

            db.session.commit()

            return redirect(url_for("pokemon.view_team_pokemon", team_id=team_id, team_index=team_index))
    else:
        flash("You do not have permission to change this move.")
        return redirect(url_for("teams.get_public_teams"))


@moves.route("/teams/<int:team_id>/<int:team_index>/<int:pokemon_move_index>/delete", methods=["POST"])
@login_required
def delete_pokemon_move_slot(team_id, team_index, pokemon_move_index):
    """
    Removes a move from a pokemon and returns the user to the pokemon view page.
    """

    team_pokemon = Teams_Pokemon.query.get((team_id, team_index))
    # Check is to prevent users from accessing the endpoint by manually entering the url if it's not their team
    if current_user.id == team_pokemon.team.owner_id:
        move = Pokemon_Moves.query.get((team_pokemon.id, team_pokemon.pokeapi_id, pokemon_move_index))
        form = RemoveMoveForm()
        if form.validate_on_submit():

            db.session.delete(move)
            db.session.commit()

            flash(f"Move successfully removed from {team_pokemon.pokemon.pokemon_name}.")

            return redirect(url_for("pokemon.view_team_pokemon", team_id=team_id, team_index=team_index))
    else:
        flash("You do not have permission to change this move.")
        return redirect(url_for("teams.get_public_teams"))
