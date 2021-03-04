import os
from unittest import TestCase

from flask import url_for
from flask_login import current_user, logout_user

from src.main import create_app, db


class CustomBaseTestClass(TestCase):
    """
    Custom test class that is responsible for setting up and tearing down test cases.
    Includes class methods for frequently used requests and auth endpoints.
    """

    @classmethod
    def setUpClass(cls):
        os.environ['FLASK_ENV'] = "testing"
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
    def get_request(cls, endpoint):
        return cls.client.get(endpoint, follow_redirects=True)

    @classmethod
    def post_request(cls, endpoint, data=None):
        return cls.client.post(endpoint, data=data, follow_redirects=True)

    @classmethod
    def login(cls, data):
        return cls.client.post(url_for("auth.login"), data=data, follow_redirects=True)

    @classmethod
    def logout(cls):
        cls.client.get(url_for("auth.logout"))
