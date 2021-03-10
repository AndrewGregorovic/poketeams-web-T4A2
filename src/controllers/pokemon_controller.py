from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from src.forms import ConfirmForm, RemovePokemonForm
from src.main import db


pokemon = Blueprint("pokemon", __name__)


@pokemon.route("/view-pokemon/select", methods=["GET"])
def get_view_pokemon_list():
    pass


@pokemon.route("/view-pokemon/<int:pokeapi_id>", methods=["GET"])
def view_selected_pokemon(pokeapi_id):
    pass


@pokemon.route("/teams/<int:team_id>/<int:team_index>", methods=["GET"])
def view_team_pokemon(team_id, team_index):
    pass


@pokemon.route("/teams/<int:team_id>/<int:team_index>/select", methods=["GET"])
@login_required
def get_team_pokemon_list(team_id, team_index):
    pass


@pokemon.route("/teams/<int:team_id>/<int:team_index>/select/<int:pokeapi_id>", methods=["GET"])
@login_required
def view_selected_team_pokemon(team_id, team_index, pokeapi_id):
    pass


@pokemon.route("/teams/<int:team_id>/<int:team_index>/edit", methods=["POST"])
@login_required
def edit_team_slot_pokemon(team_id, team_index):
    pass


@pokemon.route("/teams/<int:team_id>/<int:team_index>/delete", methods=["POST"])
@login_required
def delete_team_slot_pokemon(team_id, team_index):
    pass
