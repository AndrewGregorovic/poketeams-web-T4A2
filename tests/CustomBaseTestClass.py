import os
import random
from unittest import TestCase

from flask import url_for
from flask_login import current_user, logout_user

from src.main import create_app, db
from src.models.Team import Team


class CustomBaseTestClass(TestCase):
    """
    Custom test class that is responsible for setting up and tearing down test cases.
    Includes class methods for frequently used requests and auth endpoints.
    """

    @classmethod
    def setUpClass(cls):
        if os.environ.get("FLASK_ENV") != "workflow":
            os.environ["FLASK_ENV"] = "testing"
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.context = cls.app.test_request_context()
        cls.context.push()
        cls.client = cls.app.test_client()

        db.create_all()
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db-custom", "seed"])

    @classmethod
    def tearDownClass(cls):
        if current_user.is_authenticated:
            logout_user()
        db.session.remove()
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db-custom", "drop"])

        cls.app_context.pop()
        cls.context.pop()

    @classmethod
    def login(cls, data):
        return cls.client.post(url_for("auth.login"), data=data)

    @classmethod
    def login_follow(cls, data):
        return cls.client.post(url_for("auth.login"), data=data, follow_redirects=True)

    @classmethod
    def logout(cls):
        return cls.client.get(url_for("auth.logout"))

    @classmethod
    def logout_follow(cls):
        return cls.client.get(url_for("auth.logout"), follow_redirects=True)

    @classmethod
    def get_team_at_least_one_pokemon(cls):
        while True:
            team = random.choice(Team.query.all())
            if len(team.team_pokemon) >= 1:
                return team

    @classmethod
    def get_random_team_pokemon(cls, team):
        if len(team.team_pokemon) == 1:
            return team.team_pokemon[0]
        else:
            return random.choice(team.team_pokemon)
