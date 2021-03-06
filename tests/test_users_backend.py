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


class TestUsersBackend(CustomBaseTestClass):
    """
    Test cases to test the backend logic of the users controller endpoints.
    """

    def test_edit_user_account_details(self):
        """
        Tests that the edit user account details endpoint correctly updates with valid form data and reports form errors.
        """

        # Valid form data, username only
        user_data1 = {"username": "tester1"}

        # Invalid form data, username too short
        user_data2 = {"username": "t1"}

        # Invalid form data, username already exists
        user_data3 = {"username": "Test User 2"}

        # Valid form data, email only
        user_data4 = {"email": "unittest1@test.com"}

        # Invalid form data, email not valid
        user_data5 = {"email": "unittest1@test"}

        # Invalid form data, email already exists
        user_data6 = {"email": "test2@test.com"}

        # Invalid form data, new password too short
        user_data7 = {
            "current_password": "123456",
            "new_password": "123",
            "confirm_password": "123"
        }

        # Invalid form data, confirm password doesn't match new password
        user_data8 = {
            "current_password": "123456",
            "new_password": "111111",
            "confirm_password": "222222"
        }

        # Invalid form data, new passwords match but current password doesn't
        user_data9 = {
            "current_password": "111111",
            "new_password": "000000",
            "confirm_password": "000000"
        }

        # Valid form data, password change only
        user_data10 = {
            "current_password": "123456",
            "new_password": "999999",
            "confirm_password": "999999"
        }

        # Valid form data, full set
        user_data11 = {
            "username": "backendtest1",
            "email": "backendtest1@test.com",
            "current_password": "999999",
            "new_password": "666666",
            "confirm_password": "666666"
        }

        with self.client as c:
            self.login({"email": "test1@test.com", "password": "123456"})

            response1 = c.post(url_for("users.edit_user_account_details"), data=user_data1, follow_redirects=True)

            self.assertEqual(response1.status_code, 200)
            self.assertEqual(current_user.username, user_data1["username"])

            response2 = c.post(url_for("users.edit_user_account_details"), data=user_data2, follow_redirects=True)

            self.assertEqual(response2.status_code, 200)
            self.assertIn(b"Field must be between 3 and 30 characters long.", response2.data)

            response3 = c.post(url_for("users.edit_user_account_details"), data=user_data3, follow_redirects=True)

            self.assertEqual(response3.status_code, 200)
            self.assertIn(b"A user already exists with that username.", response3.data)

            response4 = c.post(url_for("users.edit_user_account_details"), data=user_data4, follow_redirects=True)

            self.assertEqual(response4.status_code, 200)
            self.assertEqual(current_user.email, user_data4["email"])

            response5 = c.post(url_for("users.edit_user_account_details"), data=user_data5, follow_redirects=True)

            self.assertEqual(response5.status_code, 200)
            self.assertIn(b"Invalid email address.", response5.data)

            response6 = c.post(url_for("users.edit_user_account_details"), data=user_data6, follow_redirects=True)

            self.assertEqual(response6.status_code, 200)
            self.assertIn(b"A user already exists with that email address.", response6.data)

            response7 = c.post(url_for("users.edit_user_account_details"), data=user_data7, follow_redirects=True)

            self.assertEqual(response7.status_code, 200)
            self.assertIn(b"Field must be at least 6 characters long.", response7.data)

            response8 = c.post(url_for("users.edit_user_account_details"), data=user_data8, follow_redirects=True)

            self.assertEqual(response8.status_code, 200)
            self.assertIn(b"Both passwords need to match.", response8.data)

            response9 = c.post(url_for("users.edit_user_account_details"), data=user_data9, follow_redirects=True)

            self.assertEqual(response9.status_code, 200)
            self.assertIn(b"Your current password is incorrect.", response9.data)

            response10 = c.post(url_for("users.edit_user_account_details"), data=user_data10, follow_redirects=True)

            self.assertEqual(response10.status_code, 200)
            self.assertTrue(current_user.check_password, user_data10["confirm_password"])

            response11 = c.post(url_for("users.edit_user_account_details"), data=user_data11, follow_redirects=True)

            self.assertEqual(response11.status_code, 200)
            self.assertEqual(current_user.username, user_data11["username"])
            self.assertEqual(current_user.email, user_data11["email"])
            self.assertTrue(current_user.check_password, user_data11["confirm_password"])

    def test_delete_user_account(self):
        """
        Tests that the delete user account endpoint correctly deletes the user from the database and logs them out.
        """

        with self.client as c:
            self.login({"email": "test3@test.com", "password": "123456"})

            self.assertTrue(current_user.is_authenticated)

            response = c.post(url_for("users.delete_user_account"), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIsNone(User.query.filter_by(email="test3@test.com").first())
            self.assertTrue(current_user.is_anonymous)
            self.assertFalse(current_user.is_authenticated)
