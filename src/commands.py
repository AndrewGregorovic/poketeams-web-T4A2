import random

from flask import Blueprint

from src.main import bcrypt, db
from src.models.User import User
from src.models.Team import Team
from src.models.Pokemon import Pokemon


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

    teams = []
    for i in range(10):
        team = Team()
        team.name = f"Team {i + 1}"
        team.is_private = random.choice([True, False])
        owner = random.choice(users)
        team.owner_id = owner.id
        owner.teams.append(team)
        teams.append(team)

    db.session.commit()

    for team in teams:
        number_of_pokemon = random.randint(0, 6)
        for i in range(number_of_pokemon):
            pokemon = Pokemon()
            pokemon.team_id = team.id
            pokemon.team_index = i + 1
            pokemon.pokemon_id = random.randint(1, 898)
            pokemon.pokemon_name = f"Random Name {i + 1}"
            pokemon.move_1_id = random.randint(1, 826)
            pokemon.move_2_id = random.randint(1, 826)
            pokemon.move_3_id = random.randint(1, 826)
            pokemon.move_4_id = random.randint(1, 826)
            team.pokemon.append(pokemon)

    db.session.commit()

    print("TABLES SEEDED")
