from flask import url_for

from src.forms import LogInForm, SignUpForm
from tests.CustomBaseTestClass import CustomBaseTestClass
from tests.helper_function import captured_templates


class TestAuthFrontend(CustomBaseTestClass):
    """
    Test cases to test the frontend template rendering and redirects of the auth controller endpoints.
    """

    def test_landing_page(self):
        """
        Tests that the landing page is rendered correctly.
        """

        with self.client as c:
            with captured_templates(self.app) as templates:
                response = c.get(url_for("auth.landing_page"))
                template, context = templates[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(template.name, "landing.html")

    def test_signup(self):
        """
        Tests that the signup page is rendered correctly, and the signup endpoint correctly redirects valid signups and renders the dashboard page.
        """

        # Test signup.html
        with self.client as c:
            with captured_templates(self.app) as templates:
                response = c.get(url_for("auth.signup"))
                template, context = templates[0]

            self.assertEqual(response.status_code, 200)
            self.assertEqual(template.name, "signup.html")
            self.assertIsInstance(context["form"], SignUpForm)

            # Test status code for redirect
            signup_data1 = {
                "username": "unittest1",
                "email": "unittest1@test.com",
                "password": "123456",
                "confirm_password": "123456"
            }

            signup_data2 = {
                "username": "unittest2",
                "email": "unittest2@test.com",
                "password": "123456",
                "confirm_password": "123456"
            }

            response = c.post(url_for("auth.signup"), data=signup_data1)

            self.assertEqual(response.status_code, 302)

            # Test when redirect is followed
            with captured_templates(self.app) as templates:
                response = c.post(url_for("auth.signup"), data=signup_data2, follow_redirects=True)
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "dashboard.html")

    def test_login(self):
        """
        Tests that the login page is rendered correctly, and the login endpoint correctly redirects valid logins and renders the dashboard page.
        """

        # Test login.html
        with self.client as c:
            with captured_templates(self.app) as templates:
                response = c.get(url_for("auth.login"))
                template, context = templates[0]

            self.assertEqual(response.status_code, 200)
            self.assertEqual(template.name, "login.html")
            self.assertIsInstance(context["form"], LogInForm)

            # Test status code for redirect
            response = self.login({"email": "test2@test.com", "password": "123456"})

            self.assertEqual(response.status_code, 302)

            self.logout()

            # Test when redirect is followed
            with captured_templates(self.app) as templates:
                response = self.login_follow({"email": "test2@test.com", "password": "123456"})
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "dashboard.html")

    def test_logout(self):
        """
        Tests that the logout endpoint correctly redirects and renders the landing page.
        """

        # Test status code for redirect
        with self.client:
            self.login({"email": "test1@test.com", "password": "123456"})

            response = self.logout()

            self.assertEqual(response.status_code, 302)

            # Test when redirect is followed
            self.login({"email": "test1@test.com", "password": "123456"})
            with captured_templates(self.app) as templates:
                response = self.logout_follow()
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "landing.html")
                self.assertIn(b"You have been successfully logged out.", response.data)
