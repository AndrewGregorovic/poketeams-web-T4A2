import random

from flask import url_for
from flask_login import current_user

# Flake8 ignored imports are required because of database relationships
# from src.models.Move import Move                            # noqa: F401
# from src.models.Pokemon import Pokemon                      
from src.models.PokemonMoves import Pokemon_Moves
from src.models.Team import Team
from src.models.TeamsPokemon import Teams_Pokemon
# from src.models.User import User
from tests.CustomBaseTestClass import CustomBaseTestClass
from tests.helper_function import captured_templates


class TestTeamsBackend(CustomBaseTestClass):
    """
    Test cases to test the backend logic of the teams controller endpoints.
    """

    def test_get_public_teams(self):
        """
        Tests that the logic for populating empty pokemon slots is correctly returning data with the correct size.
        """

        with self.client as c:
            with captured_templates(self.app) as templates:
                response = c.get(url_for("teams.get_public_teams"))
                template, context = templates[0]

                for team in context["teams"]:
                    self.assertEqual(len(team["team_pokemon"]), 6)

    def test_create_team(self):
        """
        Tests that the create team endpoint correctly inserts new teams into the database and reports form errors.
        """

        # Valid form data, "" is a false value for the boolean field
        team_data1 = {
            "team_name": "test team 1",
            "description": "testing creating new team",
            "is_private": ""
        }

        # Invalid form data, team name too short
        team_data2 = {
            "team_name": "t2",
            "description": "testing creating new team",
            "is_private": ""
        }

        # Invalid form data, description too long
        team_data3 = {
            "team_name": "test team 3",
            "description": """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec mollis tempor quam, at dictum ex consectetur eu.
Nullam orci dolor, commodo ac risus non, molestie interdum neque. Ut cursus est at pharetra gravida. Praesent
eget aliquam quam. Aliquam finibus metus vitae purus lacinia venenatis. In congue maximus interdum. Proin
ullamcorper arcu vitae ornare lacinia. Cras tempus volutpat metus sit amet venenatis. Praesent porta, velit eget
efficitur mollis, sapien ante bibendum neque, vitae finibus arcu nisl ut nunc. Morbi maximus nisl vitae nunc ultricies,
nec euismod lorem dignissim. Nullam posuere nisl nec orci ornare suscipit. Nunc quis ligula ultricies, tincidunt tellus
nec, porttitor neque. Vestibulum eu interdum felis. Suspendisse a interdum neque. Suspendisse condimentum ante
sed dignissim egestas. Pellentesque commodo nisi sit amet neque facilisis, quis lobortis magna ullamcorper. Nulla
sapien nibh, vulputate eget sollicitudin at, sagittis non erat. Cras quis ultricies nisl, ut volutpat metus. Pellentesque
ac venenatis nunc, in eleifend velit. Donec ullamcorper, dui sodales sodales ultrices, enim enim tincidunt lacus, a
sollicitudin massa ipsum eget arcu. Aliquam feugiat fringilla orci, tristique faucibus mauris tincidunt et. Cras bibendum,
ante sed auctor condimentum, enim nibh varius sem, a scelerisque ligula nibh eget neque. Vestibulum et urna at enim
molestie lacinia. Praesent laoreet felis a felis pharetra bibendum. In ex neque, dignissim et dapibus non, aliquam vel
sapien. Quisque ipsum nisl, tempus eu ex sed, feugiat convallis nisl. Curabitur porttitor justo et lacus faucibus convallis.
Donec aliquam, massa non feugiat tempus, risus turpis consectetur elit, sit amet convallis lorem erat vel neque.
Suspendisse non sapien ac dolor tempor semper eu et lorem. Nullam sollicitudin sapien quis mollis ultricies. Etiam
lacinia dapibus est, id volutpat enim imperdiet a. Proin pellentesque, felis vitae molestie luctus, massa risus blandit
mi, quis fermentum ligula. Donec ullamcorper.""",
            "is_private": False
        }

        with self.client as c:
            self.login({"email": f"test{random.randint(1, 5)}@test.com", "password": "123456"})
            response1 = c.post(url_for("teams.create_team"), data=team_data1, follow_redirects=True)

            self.assertEqual(response1.status_code, 200)
            self.assertIsNotNone(Team.query.filter_by(name=team_data1["team_name"]).first())
            self.assertIsInstance(Team.query.filter_by(name=team_data1["team_name"]).first(), Team)
            self.assertEqual(Team.query.filter_by(name=team_data1["team_name"]).first().is_private, False)

            response2 = c.post(url_for("teams.create_team"), data=team_data2, follow_redirects=True)

            self.assertEqual(response2.status_code, 200)
            self.assertIn(b"Field must be between 3 and 50 characters long.", response2.data)

            response3 = c.post(url_for("teams.create_team"), data=team_data3, follow_redirects=True)

            self.assertEqual(response3.status_code, 200)
            self.assertIn(b"Field cannot be longer than 2000 characters.", response3.data)

    def test_get_team(self):
        """
        Tests that the logic for populating empty pokemon and move slots is correctly returning data with the correct size.
        """

        with self.client as c:
            team = random.choice(Team.query.filter_by(is_private=False).all())

            with captured_templates(self.app) as templates:
                response = c.get(url_for("teams.get_team", team_id=team.id))
                template, context = templates[0]

                self.assertEqual(len(context["team"]["team_pokemon"]), 6)
                self.assertEqual(len(context["move_sets"]), 6)
                for move_set in context["move_sets"]:
                    if move_set:
                        self.assertEqual(len(move_set), 4)

    def test_edit_team_details(self):
        """
        Tests that the edit team details endpoint correctly updates the team with valid form data and reports form errors.
        """

        # Valid form data, "" is a false value for the boolean field
        edit_data1 = {
            "team_name": "edited team 1",
            "description": "testing editing team details",
            "is_private": ""
        }

        # Invalid form data, team name too short
        edit_data2 = {
            "team_name": "e2",
            "description": "testing editing team details",
            "is_private": ""
        }

        # Invalid form data, description too long
        edit_data3 = {
            "team_name": "edited team 3",
            "description": """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec mollis tempor quam, at dictum ex consectetur eu.
Nullam orci dolor, commodo ac risus non, molestie interdum neque. Ut cursus est at pharetra gravida. Praesent
eget aliquam quam. Aliquam finibus metus vitae purus lacinia venenatis. In congue maximus interdum. Proin
ullamcorper arcu vitae ornare lacinia. Cras tempus volutpat metus sit amet venenatis. Praesent porta, velit eget
efficitur mollis, sapien ante bibendum neque, vitae finibus arcu nisl ut nunc. Morbi maximus nisl vitae nunc ultricies,
nec euismod lorem dignissim. Nullam posuere nisl nec orci ornare suscipit. Nunc quis ligula ultricies, tincidunt tellus
nec, porttitor neque. Vestibulum eu interdum felis. Suspendisse a interdum neque. Suspendisse condimentum ante
sed dignissim egestas. Pellentesque commodo nisi sit amet neque facilisis, quis lobortis magna ullamcorper. Nulla
sapien nibh, vulputate eget sollicitudin at, sagittis non erat. Cras quis ultricies nisl, ut volutpat metus. Pellentesque
ac venenatis nunc, in eleifend velit. Donec ullamcorper, dui sodales sodales ultrices, enim enim tincidunt lacus, a
sollicitudin massa ipsum eget arcu. Aliquam feugiat fringilla orci, tristique faucibus mauris tincidunt et. Cras bibendum,
ante sed auctor condimentum, enim nibh varius sem, a scelerisque ligula nibh eget neque. Vestibulum et urna at enim
molestie lacinia. Praesent laoreet felis a felis pharetra bibendum. In ex neque, dignissim et dapibus non, aliquam vel
sapien. Quisque ipsum nisl, tempus eu ex sed, feugiat convallis nisl. Curabitur porttitor justo et lacus faucibus convallis.
Donec aliquam, massa non feugiat tempus, risus turpis consectetur elit, sit amet convallis lorem erat vel neque.
Suspendisse non sapien ac dolor tempor semper eu et lorem. Nullam sollicitudin sapien quis mollis ultricies. Etiam
lacinia dapibus est, id volutpat enim imperdiet a. Proin pellentesque, felis vitae molestie luctus, massa risus blandit
mi, quis fermentum ligula. Donec ullamcorper.""",
            "is_private": ""
        }

        with self.client as c:
            team = random.choice(Team.query.all())
            self.login({"email": f"test{team.owner_id}@test.com", "password": "123456"})

            response1 = c.post(url_for("teams.edit_team_details", team_id=team.id), data=edit_data1, follow_redirects=True)

            self.assertEqual(response1.status_code, 200)
            self.assertEqual(team.name, edit_data1["team_name"])
            self.assertEqual(team.description, edit_data1["description"])
            self.assertEqual(team.is_private, False)

            response2 = c.post(url_for("teams.edit_team_details", team_id=team.id), data=edit_data2, follow_redirects=True)

            self.assertEqual(response2.status_code, 200)
            self.assertIn(b"Field must be between 3 and 50 characters long.", response2.data)

            response3 = c.post(url_for("teams.edit_team_details", team_id=team.id), data=edit_data3, follow_redirects=True)

            self.assertEqual(response3.status_code, 200)
            self.assertIn(b"Field cannot be longer than 2000 characters.", response3.data)

    def test_delete_team(self):
        """
        Tests that the delete team endpoint correctly deletes the team and its children from the database.
        """

        with self.client as c:
            team = random.choice(Team.query.all())
            self.login({"email": f"test{team.owner_id}@test.com", "password": "123456"})

            response = c.post(url_for("teams.delete_team", team_id=team.id), follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            # Check team was deleted
            self.assertIsNone(Team.query.filter_by(id=team.id).first())

            # Check child teams_pokemon database entries were deleted
            self.assertEqual(len(Teams_Pokemon.query.filter_by(team_id=team.id).all()), 0)

            # Check child pokemon_moves database entries were deleted
            for pokemon in team.team_pokemon:
                self.assertEqual(len(Pokemon_Moves.query.filter_by(team_pokemon_id=pokemon.id).all()), 0)
