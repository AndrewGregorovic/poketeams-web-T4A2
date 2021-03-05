from flask import url_for

from src.forms import DeleteUserAccountForm, EditUserAccountForm
from tests.CustomBaseTestClass import CustomBaseTestClass
from tests.helper_function import captured_templates


class TestUsersFrontend(CustomBaseTestClass):
    """
    Test cases to test the frontend template rendering and redirects of the users controller endpoints.
    """

    def test_dashboard(self):
        """
        Tests that the dashboard page is rendered correctly.
        """

        with self.client as c:
            self.login({"email": "test1@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("users.dashboard"))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "dashboard.html")

    def test_get_user_account_details(self):
        """
        Tests that the user account details page is rendered correctly.
        """

        with self.client as c:
            self.login({"email": "test1@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("users.get_user_account_details"))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "account.html")
                self.assertIsInstance(context["form"], DeleteUserAccountForm)

    def test_edit_user_account_details(self):
        """
        Tests that the edit user account details page is rendered correctly, and the endpoint correctly redirects on valid form data and renders the account details page.
        """

        # Test account_edit.html
        with self.client as c:
            self.login({"email": "test1@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("users.edit_user_account_details"))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "account_edit.html")
                self.assertIsInstance(context["form"], EditUserAccountForm)

            # Test status code for redirect
            edit_data1 = {"username": "tester1"}
            edit_data2 = {"username": "unittest1"}

            response = c.post(url_for("users.edit_user_account_details"), data=edit_data1)

            self.assertEqual(response.status_code, 302)

            # Test when redirect is followed
            with captured_templates(self.app) as templates:
                response = c.post(url_for("users.edit_user_account_details"), data=edit_data2, follow_redirects=True)
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "account.html")

    def test_delete_user_account(self):
        """
        Tests that the delete user account endpoint correctly redirects and renders the landing page.
        """

        # Test status code for redirect
        with self.client as c:
            self.login({"email": "test5@test.com", "password": "123456"})
            response = c.post(url_for("users.delete_user_account"))

            self.assertEqual(response.status_code, 302)

            # Test when redirect is followed
            self.login({"email": "test4@test.com", "password": "123456"})
            with captured_templates(self.app) as templates:
                response = c.post(url_for("users.delete_user_account"), follow_redirects=True)
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "landing.html")
