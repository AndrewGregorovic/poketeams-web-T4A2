import random

from flask import Blueprint

from src.main import bcrypt, db
from src.models.User import User
from src.models.Team import Team
from src.models.TeamsPokemon import Teams_Pokemon
from src.models.Pokemon import Pokemon
from src.models.PokemonMoves import Pokemon_Moves
from src.models.Move import Move


db_commands = Blueprint("db-custom", __name__)


@db_commands.cli.command("create")
def create_db():
    """
    Custom flask db command to create all tables from models
    """

    db.create_all()
    print("TABLES CREATED")


@db_commands.cli.command("drop")
def drop_db():
    """
    Custom flask db command to drop all tables from the database
    """

    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("TABLES DROPPED")


@db_commands.cli.command("seed")
def seed_db():
    """
    Custom flask db command to seed tables with fake data for testing
    """

    users = []
    for i in range(5):
        user = User()
        user.username = f"Test User {i + 1}"
        user.email = f"test{i + 1}@test.com"
        user.password = bcrypt.generate_password_hash("123456").decode("utf-8")
        db.session.add(user)
        users.append(user)

    db.session.commit()

    team_list = []
    for i in range(10):
        team = Team()
        team.name = f"Team {i + 1}"

        # Make sure there is always at least 1 public/private team
        if i == 8:
            team.is_private = False
        elif i == 9:
            team.is_private = True
        else:
            team.is_private = random.choice([True, False])
        owner = random.choice(users)
        team.owner_id = owner.id
        owner.teams.append(team)
        team_list.append(team)

    db.session.commit()

    pokemon_list = []
    for team in team_list:
        number_of_pokemon = random.randint(0, 6)
        for i in range(number_of_pokemon):
            pokemon = Pokemon()
            pokemon.pokemon_id = random.randint(1, 898)
            pokemon.pokeapi_id = pokemon.pokemon_id
            pokemon.pokemon_name = f"Random Name {i + 1}"
            if pokemon.pokeapi_id not in [pokemon.pokeapi_id for pokemon in pokemon_list]:
                db.session.add(pokemon)
            pokemon_list.append(pokemon)

            team_pokemon = Teams_Pokemon()
            team_pokemon.team_id = team.id
            team_pokemon.team_index = i + 1
            team_pokemon.pokeapi_id = pokemon.pokemon_id
            team.team_pokemon.append(team_pokemon)

    db.session.commit()

    move_list = []
    for team in team_list:
        number_of_moves = random.randint(0, 4)
        for team_pokemon in team.team_pokemon:
            for i in range(number_of_moves):
                move = Move()
                move.move_id = random.randint(1, 826)
                move.move_name = f"Random Move {i + 1}"
                if move.move_id not in [move.move_id for move in move_list]:
                    db.session.add(move)
                move_list.append(move)

                pokemon_move = Pokemon_Moves()
                pokemon_move.team_pokemon_id = team_pokemon.id
                pokemon_move.pokeapi_id = team_pokemon.pokemon.pokeapi_id
                pokemon_move.pokemon_move_index = i + 1
                pokemon_move.move_id = move.move_id
                db.session.add(pokemon_move)

    db.session.commit()

    print("TABLES SEEDED")
