import random

from flask import url_for

from src.forms import CreateTeamForm, DeleteTeamForm, EditTeamForm
from src.models.Team import Team
from tests.CustomBaseTestClass import CustomBaseTestClass
from tests.helper_function import captured_templates


class TestTeamsFrontend(CustomBaseTestClass):
    """
    Test cases to test the frontend template rendering and redirects of the teams controller endpoints.
    """

    def test_get_users_teams(self):
        """
        Tests that the my teams page is rendered correctly.
        """

        with self.client as c:
            self.login({"email": f"test{random.randint(1, 5)}@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("teams.get_users_teams"))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "team_list.html")
                self.assertIn(b"My Pokemon Teams", response.data)

    def test_get_public_teams(self):
        """
        Tests that the public teams page is rendered correctly.
        """

        with self.client as c:
            with captured_templates(self.app) as templates:
                response = c.get(url_for("teams.get_public_teams"))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "team_list.html")
                self.assertIn(b"Public Pokemon Teams", response.data)

    def test_create_team(self):
        """
        Tests that the create team page is rendered correctly, and the endpoint correctly redirects on valid form data and renders the team view page.
        """

        team_data1 = {
            "team_name": "test 1",
            "description": "first team testing creation",
            "is_private": False
        }
        team_data2 = {
            "team_name": "test 2",
            "description": "second team testing creation",
            "is_private": True
        }

        # Test team_create.html
        with self.client as c:
            self.login({"email": f"test{random.randint(1, 5)}@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("teams.create_team"))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "team_create.html")
                self.assertIsInstance(context["form"], CreateTeamForm)

            # Test status code for redirect
            response = c.post(url_for("teams.create_team"), data=team_data1)

            self.assertEqual(response.status_code, 302)

            # Test when redirect is followed
            with captured_templates(self.app) as templates:
                response = c.post(url_for("teams.create_team"), data=team_data2, follow_redirects=True)
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "team_view.html")

    def test_get_team(self):
        """
        Tests that the team view page is rendered correctly.
        """

        with self.client as c:

            # Test the team view of a users private team
            team = random.choice(Team.query.filter_by(is_private=True).all())
            self.login({"email": f"test{team.owner_id}@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("teams.get_team", team_id=team.id))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "team_view.html")
                self.assertIsInstance(context["form"], DeleteTeamForm)
                self.assertIn(b"Private", response.data)
                self.assertIn(b"Edit Team Details", response.data)
                self.assertIn(b"Delete Team", response.data)
                self.assertIn(bytes(team.name, "utf-8"), response.data)

            self.logout()

            # Test the team view of a users public team
            team = random.choice(Team.query.filter_by(is_private=False).all())
            self.login({"email": f"test{team.owner_id}@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("teams.get_team", team_id=team.id))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "team_view.html")
                self.assertIsInstance(context["form"], DeleteTeamForm)
                self.assertIn(b"Public", response.data)
                self.assertIn(b"Edit Team Details", response.data)
                self.assertIn(b"Delete Team", response.data)
                self.assertIn(bytes(team.name, "utf-8"), response.data)

            self.logout()

            # Test the team view of a public team by another user or anonymous user
            team = random.choice(Team.query.filter_by(is_private=False).all())

            with captured_templates(self.app) as templates:
                response = c.get(url_for("teams.get_team", team_id=team.id))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "team_view.html")
                self.assertNotIn(b"Private", response.data)
                self.assertIn(bytes(team.owner.username, "utf-8"), response.data)
                self.assertNotIn(b"Edit Team Details", response.data)
                self.assertNotIn(b"Delete Team", response.data)
                self.assertIn(bytes(team.name, "utf-8"), response.data)

    def test_edit_team_details(self):
        """
        Tests that the edit team page is rendered correctly, and the endpoint correctly redirects on valid form data and renders the team view page.
        """

        edit_data1 = {
            "team_name": "edit 1",
            "description": "testing editing team details",
            "is_private": False
        }
        edit_data2 = {
            "team_name": "edit 2",
            "description": "testing editing team details",
            "is_private": True
        }

        # Test team_edit.html
        with self.client as c:
            team = random.choice(Team.query.all())
            self.login({"email": f"test{team.owner_id}@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("teams.edit_team_details", team_id=team.id))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "team_edit.html")
                self.assertIsInstance(context["form"], EditTeamForm)

            # Test status code for redirect
            response = c.post(url_for("teams.create_team"), data=edit_data1)

            self.assertEqual(response.status_code, 302)

            # Test when redirect is followed
            with captured_templates(self.app) as templates:
                response = c.post(url_for("teams.edit_team_details", team_id=team.id), data=edit_data2, follow_redirects=True)
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "team_view.html")

    def test_delete_team(self):
        """
        Tests that the delete team endpoint correctly redirects and renders the my teams page.
        """

        # Test status code for redirect
        with self.client as c:
            team = random.choice(Team.query.all())
            self.login({"email": f"test{team.owner_id}@test.com", "password": "123456"})
            response = c.post(url_for("teams.delete_team", team_id=team.id))

            self.assertEqual(response.status_code, 302)

            self.logout()

            # Test when redirect is followed
            team = random.choice(Team.query.all())
            self.login({"email": f"test{team.owner_id}@test.com", "password": "123456"})
            with captured_templates(self.app) as templates:
                response = c.post(url_for("teams.delete_team", team_id=team.id), follow_redirects=True)
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "team_list.html")
                self.assertIn(b"My Pokemon Teams", response.data)
