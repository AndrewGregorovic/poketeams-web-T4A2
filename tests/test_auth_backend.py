from flask import url_for
from flask_login import current_user

# Flake8 ignored imports are required because of database relationships
from src.models.Move import Move                            # noqa: F401
from src.models.Pokemon import Pokemon                      # noqa: F401
from src.models.PokemonMoves import Pokemon_Moves           # noqa: F401
from src.models.Team import Team                            # noqa: F401
from src.models.TeamsPokemon import Teams_Pokemon           # noqa: F401
from src.models.User import User
from tests.CustomBaseTestClass import CustomBaseTestClass


class TestAuthBackend(CustomBaseTestClass):
    """
    Test cases to test the backend logic of the auth controller endpoints.
    """

    def test_signup(self):
        """
        Tests that the signup endpoint correctly registers new users in the database and reports form errors.
        """

        # Valid form data
        user_data1 = {
            "username": "unittest",
            "email": "unittest@test.com",
            "password": "123456",
            "confirm_password": "123456"
        }

        # Invalid form data, username too short
        user_data2 = {
            "username": "ut",
            "email": "unittest@test.com",
            "password": "123456",
            "confirm_password": "123456"
        }

        # Invalid form data, username too long
        user_data3 = {
            "username": "unittestunittestunittestunittest",
            "email": "unittest@test.com",
            "password": "123456",
            "confirm_password": "123456"
        }

        # Invalid form data, invalid email address
        user_data4 = {
            "username": "unittest",
            "email": "unittest@test",
            "password": "123456",
            "confirm_password": "123456"
        }

        # Invalid form data, password too short
        user_data5 = {
            "username": "unittest",
            "email": "unittest@test.com",
            "password": "123",
            "confirm_password": "123"
        }

        # Invalid form data, passwords don't match
        user_data6 = {
            "username": "unittest",
            "email": "unittest@test.com",
            "password": "123456",
            "confirm_password": "111111"
        }

        # Invalid form data, username already exists
        user_data7 = {
            "username": "Test User 1",
            "email": "unittest@test.com",
            "password": "123456",
            "confirm_password": "123456"
        }

        # Invalid form data, email already exists
        user_data8 = {
            "username": "test1",
            "email": "test1@test.com",
            "password": "123456",
            "confirm_password": "123456"
        }

        with self.client:
            response1 = self.post_request(url_for("auth.signup"), user_data1)
            response2 = self.post_request(url_for("auth.signup"), user_data2)
            response3 = self.post_request(url_for("auth.signup"), user_data3)
            response4 = self.post_request(url_for("auth.signup"), user_data4)
            response5 = self.post_request(url_for("auth.signup"), user_data5)
            response6 = self.post_request(url_for("auth.signup"), user_data6)
            response7 = self.post_request(url_for("auth.signup"), user_data7)
            response8 = self.post_request(url_for("auth.signup"), user_data8)

            self.assertEqual(response1.status_code, 200)
            self.assertIsNotNone(User.query.filter_by(username=user_data1["username"], email=user_data1["email"]).first())
            self.assertIsInstance(User.query.filter_by(username=user_data1["username"], email=user_data1["email"]).first(), User)

            self.assertEqual(response2.status_code, 200)
            self.assertIn(b"Field must be between 3 and 30 characters long.", response2.data)

            self.assertEqual(response3.status_code, 200)
            self.assertIn(b"Field must be between 3 and 30 characters long.", response3.data)

            self.assertEqual(response4.status_code, 200)
            self.assertIn(b"Invalid email address.", response4.data)

            self.assertEqual(response5.status_code, 200)
            self.assertIn(b"Field must be at least 6 characters long.", response5.data)

            self.assertEqual(response6.status_code, 200)
            self.assertIn(b"Both passwords need to match.", response6.data)

            self.assertEqual(response7.status_code, 200)
            self.assertIn(b"A user already exists with that username.", response7.data)

            self.assertEqual(response8.status_code, 200)
            self.assertIn(b"A user already exists with that email address.", response8.data)

    def test_login(self):
        """
        Tests that the login endpoint correctly logs in users and reports form errors.
        """

        # Valid form data
        user_data1 = {
            "email": "test4@test.com",
            "password": "123456",
        }

        # Invalid form data, incorrect username
        user_data2 = {
            "email": "test44@test.com",
            "password": "123456",
        }

        # Invalid form data, incorrect password
        user_data3 = {
            "email": "test4@test.com",
            "password": "222222",
        }

        with self.client:
            response1 = self.login_follow(user_data1)

            self.assertEqual(response1.status_code, 200)
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.username, "Test User 4")
            self.assertEqual(current_user.email, "test4@test.com")

            self.logout()

            response2 = self.login_follow(user_data2)

            self.assertTrue(current_user.is_anonymous)
            self.assertEqual(response2.status_code, 200)
            self.assertIn(b"Invalid email and password.", response2.data)

            response3 = self.login_follow(user_data3)
            
            self.assertTrue(current_user.is_anonymous)
            self.assertEqual(response3.status_code, 200)
            self.assertIn(b"Invalid email and password.", response3.data)

    def test_logout(self):
        """
        Tests that the logout endpoint correctly logs out an authenticated user.
        """

        with self.client:
            self.login({"email": "test3@test.com", "password": "123456"})

            self.assertTrue(current_user.is_authenticated)

            response = self.logout_follow()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(current_user.is_anonymous)
            self.assertFalse(current_user.is_authenticated)
