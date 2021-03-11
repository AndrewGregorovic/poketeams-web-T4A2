from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from src.forms import ConfirmForm, RemoveMoveForm
from src.main import db


moves = Blueprint("moves", __name__)


@moves.route("/teams/<int:team_id>/<int:team_index>/<int:pokemon_move_index>", methods=["GET"])
def view_pokemon_move(team_id, team_index, pokemon_move_index):
    pass


@moves.route("/teams/<int:team_id>/<int:team_index>/<int:pokemon_move_index>/select", methods=["GET"])
@login_required
def get_pokemon_move_list(team_id, team_index, pokemon_move_index):
    pass


@moves.route("/teams/<int:team_id>/<int:team_index>/<int:pokemon_move_index>/select/<int:move_id>", methods=["GET"])
@login_required
def view_selected_pokemon_move(team_id, team_index, pokemon_move_index, move_id):
    pass


@moves.route("/teams/<int:team_id>/<int:team_index>/<int:pokemon_move_index>/edit", methods=["POST"])
@login_required
def edit_pokemon_move_slot(team_id, team_index, pokemon_move_index):
    pass


@moves.route("/teams/<int:team_id>/<int:team_index>/<int:pokemon_move_index>/delete", methods=["POST"])
@login_required
def delete_pokemon_move_slot(team_id, team_index, pokemon_move_index):
    pass
