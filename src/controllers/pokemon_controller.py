from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from src.forms import ConfirmForm, RemovePokemonForm
from src.main import db
from src.models.Pokemon import Pokemon
from src.models.PokemonMoves import Pokemon_Moves
from src.models.Team import Team
from src.models.TeamsPokemon import Teams_Pokemon
from src.schemas.PokemonMovesSchema import pokemon_moves_schema
from src.schemas.TeamsPokemonSchema import teams_pokemon_schema


pokemon = Blueprint("pokemon", __name__)


@pokemon.route("/view-pokemon/select", methods=["GET"])
def get_view_pokemon_list():
    """
    Returns the pokemon list page for looking up a pokemons pokedex entry without needing to create a team.
    """

    api_data = Pokemon.get_pokedex_list()
    return render_template("pokemon_select.html", data=api_data, type="pokedex")


@pokemon.route("/view-pokemon/<int:pokeapi_id>", methods=["GET"])
def view_selected_pokemon(pokeapi_id):
    """
    Returns the pokedex entry page for the pokemon selected on the previous pokemon list page.
    """

    pokemon_api_data = Pokemon.get_pokemon_data(pokeapi_id)
    ability_data = [Pokemon.get_pokemon_ability_data(ability["ability"]["url"]) for ability in pokemon_api_data["abilities"]]
    return render_template("pokemon_view.html", data=[pokemon_api_data, ability_data], pokeapi_id=pokeapi_id, type="pokedex")


@pokemon.route("/teams/<int:team_id>/<int:team_index>", methods=["GET"])
def view_team_pokemon(team_id, team_index):
    """
    Returns the pokemon view page for a pokemon on a team.
    """

    form = RemovePokemonForm()
    team = Team.query.get(team_id)
    team_pokemon = Teams_Pokemon.query.get((team_id, team_index))

    # If pokemon slot is empty skip the pokemon view and go to the pokemon list page to select a pokemon
    if not team_pokemon:
        return redirect(url_for("pokemon_select.html", team_id=team_id, team_index=team_index))
    else:
        pokemon_api_data = Pokemon.get_pokemon_data(team_pokemon.pokeapi_id)

        # Get the pokemons currently assigned moves and insert null entries for move slots that are empty
        move_set = Pokemon_Moves.query.filter_by(team_pokemon_id=team_pokemon.id).order_by(Pokemon_Moves.pokemon_move_index).all()
        move_set_dict = pokemon_moves_schema.dump(move_set)
        indices = [move.pokemon_move_index for move in move_set]
        for i in range(4):
            if i + 1 not in indices:
                move_set_dict.insert(i, None)

        ability_data = [Pokemon.get_pokemon_ability_data(ability["ability"]["url"]) for ability in pokemon_api_data["abilities"]]
        data = [pokemon_api_data, ability_data]
        return render_template("pokemon_view.html", data=data, form=form, moves=move_set_dict, team_pokemon=team_pokemon, 
                               team=team, team_id=team_id, team_index=team_index, type="team")


@pokemon.route("/teams/<int:team_id>/<int:team_index>/select", methods=["GET"])
@login_required
def get_team_pokemon_list(team_id, team_index):
    """
    Returns the pokemon list page for a team pokemon slot.
    """

    team = Team.query.get(team_id)

    # Get current pokemon as the back button on the template will need a different url if the current pokemon is empty
    current_pokemon = Teams_Pokemon.query.get((team_id, team_index))

    # Check is to prevent users from accessing the endpoint by manually entering the url if it's not their team
    if current_user.id == team.owner_id:
        api_data = Pokemon.get_pokedex_list()
        return render_template("pokemon_select.html", data=api_data, current_pokemon=current_pokemon, team=team,
                               team_id=team_id, team_index=team_index, type="team")
    else:
        flash("You do not have permission to change this pokemon.")
        return redirect(url_for("teams.get_public_teams"))


@pokemon.route("/teams/<int:team_id>/<int:team_index>/select/<int:pokeapi_id>", methods=["GET"])
@login_required
def view_selected_team_pokemon(team_id, team_index, pokeapi_id):
    """
    Returns the pokemon view page for pokemon selected on the previous pokemon select page.
    """

    team = Team.query.get(team_id)
    # Check is to prevent users from accessing the endpoint by manually entering the url if it's not their team
    if current_user.id == team.owner_id:
        form = ConfirmForm()
        pokemon_api_data = Pokemon.get_pokemon_data(pokeapi_id)
        ability_data = [Pokemon.get_pokemon_ability_data(ability["ability"]["url"]) for ability in pokemon_api_data["abilities"]]
        return render_template("pokemon_view.html", data=[pokemon_api_data, ability_data], form=form, team=team, team_id=team_id,
                               team_index=team_index, pokeapi_id=pokeapi_id, type="team-selected")

    else:
        flash("You do not have permission to change this pokemon.")
        return redirect(url_for("teams.get_public_teams"))


@pokemon.route("/teams/<int:team_id>/<int:team_index>/edit/<int:pokeapi_id>", methods=["POST"])
@login_required
def edit_team_slot_pokemon(team_id, team_index, pokeapi_id):
    """
    Adds a new pokemon to a team or updates an existing pokemon, when updating all child entries are deleted.
    """

    team = Team.query.get(team_id)
    # Check is to prevent users from accessing the endpoint by manually entering the url if it's not their team
    if current_user.id == team.owner_id:
        form = ConfirmForm()
        if form.validate_on_submit():

            # Create new entry if pokemon not already in database
            pokemon = Pokemon.query.get(pokeapi_id)
            if not pokemon:
                pokemon_api_data = Pokemon.get_pokemon_data(pokeapi_id)
                pokemon = Pokemon()
                pokemon.pokeapi_id = pokeapi_id
                pokemon.pokemon_id = int(pokemon_api_data["species"]["url"].replace("https://pokeapi.co/api/v2/pokemon-species/", "").replace("/", ""))
                pokemon.pokemon_name = pokemon_api_data["name"].capitalize()
                db.session.add(pokemon)
                db.session.commit()

            # Create new entry if there is no existing team_pokemon for this team id and team index,
            # otherwise update the existing entry
            team_pokemon = Teams_Pokemon.query.filter_by(team_id=team_id, team_index=team_index).first()
            if not team_pokemon:
                new_team_pokemon = Teams_Pokemon()
                new_team_pokemon.team_id = team_id
                new_team_pokemon.team_index = team_index
                new_team_pokemon.pokeapi_id = pokeapi_id
                team.team_pokemon.append(new_team_pokemon)
            else:
                teams_pokemon = Teams_Pokemon.query.filter_by(team_id=team_id, team_index=team_index)
                data = {
                    "team_id": team_id,
                    "team_index": team_index,
                    "pokeapi_id": pokemon.pokeapi_id
                }

                teams_pokemon.update(teams_pokemon_schema.load(data, partial=True))

                # Delete the saved moves of the old pokemon
                pokemon_moves = Pokemon_Moves.query.filter_by(team_pokemon_id=teams_pokemon[0].id)
                for move in pokemon_moves:
                    db.session.delete(move)

            db.session.commit()

            return redirect(url_for("pokemon.view_team_pokemon", team_id=team_id, team_index=team_index))
    else:
        flash("You do not have permission to change this pokemon.")
        return redirect(url_for("teams.get_public_teams"))


@pokemon.route("/teams/<int:team_id>/<int:team_index>/delete", methods=["POST"])
@login_required
def delete_team_slot_pokemon(team_id, team_index):
    """
    Deletes a pokemon from a team along with any moves that have been assigned to it.
    """

    team_pokemon = Teams_Pokemon.query.get((team_id, team_index))
    # Check is to prevent users from accessing the endpoint by manually entering the url if it's not their team
    if current_user.id == team_pokemon.team.owner_id:
        form = RemovePokemonForm()
        if form.validate_on_submit():

            db.session.delete(team_pokemon)
            db.session.commit()

            flash(f"Pokemon successfully removed from {team_pokemon.team.name}, Slot {team_index}.")

            return redirect(url_for("teams.get_team", team_id=team_id))
    else:
        flash("You do not have permission to remove this pokemon from the team.")
        return redirect(url_for("teams.get_public_teams"))
