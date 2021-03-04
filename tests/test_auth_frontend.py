from flask import url_for

from src.forms import LogInForm, SignUpForm
from tests.CustomBaseTestClass import CustomBaseTestClass
from tests.helper_function import captured_templates


class TestAuthFrontend(CustomBaseTestClass):
    """
    Test cases to test the frontend side of the auth controller endpoints.
    """

    def test_landing_page(self):
        """
        Tests that the landing page is rendered correctly.
        """

        with captured_templates(self.app) as templates:
            response = self.client.get(url_for("auth.landing_page"))
            template, context = templates[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(template.name, 'landing.html')

    def test_signup(self):
        """
        Tests that the signup page is rendered correctly.
        """

        with captured_templates(self.app) as templates:
            response = self.client.get(url_for("auth.signup"))
            template, context = templates[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(template.name, 'signup.html')
        self.assertIsInstance(context["form"], SignUpForm)

    def test_login(self):
        """
        Tests that the login page is rendered correctly.
        """

        with captured_templates(self.app) as templates:
            response = self.client.get(url_for("auth.login"))
            template, context = templates[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(template.name, 'login.html')
        self.assertIsInstance(context["form"], LogInForm)

    def test_logout(self):
        """
        Tests that the logout endpoint correctly redirects.
        """

        self.login({"email": "test1@test.com", "password": "123456"})
        response = self.client.get(url_for("auth.logout"))

        self.assertEqual(response.status_code, 302)
