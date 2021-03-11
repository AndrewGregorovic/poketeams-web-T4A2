import random

from flask import url_for

from src.forms import ConfirmForm, RemovePokemonForm
from tests.CustomBaseTestClass import CustomBaseTestClass
from tests.helper_function import captured_templates


class TestPokemonFrontend(CustomBaseTestClass):
    """
    Test cases to test the frontend template rendering and redirects of the pokemon controller endpoints.
    """

    def test_get_view_pokemon_list(self):
        """
        Tests that the pokedex version of the pokemon list page is rendered correctly.
        """

        with self.client as c:
            with captured_templates(self.app) as templates:
                response = c.get(url_for("pokemon.get_view_pokemon_list"))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "pokemon_select.html")
                self.assertNotIn(b"Slot", response.data)

    def test_view_selected_pokemon(self):
        """
        Tests that the pokedex version of the pokemon view page is rendered correctly.
        """

        with self.client as c:
            with captured_templates(self.app) as templates:
                response = c.get(url_for("pokemon.view_selected_pokemon", pokeapi_id=random.randint(1, 898)))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "pokemon_view.html")
                self.assertIn(b"Pokedex Entry", response.data)

    def test_view_team_pokemon(self):
        """
        Tests that the team version of the pokemon view page is rendered correctly.
        """

        with self.client as c:

            # Test the view of a pokemon on a users team
            team_pokemon = self.get_random_team_pokemon()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("pokemon.view_team_pokemon", team_id=team_pokemon.team_id, team_index=team_pokemon.team_index))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "pokemon_view.html")
                self.assertIsInstance(context["form"], RemovePokemonForm)
                self.assertIn(b"Change Pokemon", response.data)
                if b"Name: Empty" not in response.data:
                    self.assertIn(b"Remove Pokemon", response.data)
                self.assertIn(bytes(team_pokemon.team.name, "utf-8"), response.data)

            self.logout()

            # Test the view of a pokemon in a public team by another user or with anonymous user
            team_pokemon = self.get_random_team_pokemon_public()

            with captured_templates(self.app) as templates:
                response = c.get(url_for("pokemon.view_team_pokemon", team_id=team_pokemon.team_id, team_index=team_pokemon.team_index))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "pokemon_view.html")
                self.assertIn(bytes(team_pokemon.team.owner.username, "utf-8"), response.data)
                self.assertNotIn(b"Change Pokemon", response.data)
                self.assertNotIn(b"Remove Pokemon", response.data)
                self.assertIn(bytes(team_pokemon.team.name, "utf-8"), response.data)

    def test_get_team_pokemon_list(self):
        """
        Tests that the team version of the pokemon list page is rendered correctly.
        """

        with self.client as c:
            team_pokemon = self.get_random_team_pokemon()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("pokemon.get_team_pokemon_list", team_id=team_pokemon.team_id, team_index=team_pokemon.team_index))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "pokemon_select.html")
                self.assertIn(bytes(team_pokemon.team.name, "utf-8"), response.data)
                self.assertIn(b"Slot", response.data)

    def test_view_selected_team_pokemon(self):
        """
        Tests that the pokemon view page for the selected pokemon is rendered correctly.
        """

        with self.client as c:
            team_pokemon = self.get_random_team_pokemon()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("pokemon.view_selected_team_pokemon", team_id=team_pokemon.team_id,
                                         team_index=team_pokemon.team_index, pokeapi_id=random.randint(1, 898)))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "pokemon_view.html")
                self.assertIsInstance(context["form"], ConfirmForm)
                self.assertIn(b"Confirm", response.data)
                self.assertIn(bytes(team_pokemon.team.name, "utf-8"), response.data)

    def test_edit_team_slot_pokemon(self):
        """
        Tests that the edit team slot pokemon endpoint correctly redirects on confirming a pokemon change and renders the team pokemon view page for that pokemon.
        """

        # Test status code for redirect
        with self.client as c:
            team_pokemon = self.get_random_team_pokemon()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})
            response = c.post(url_for("pokemon.edit_team_slot_pokemon", team_id=team_pokemon.team_id,
                                      team_index=team_pokemon.team_index, pokeapi_id=random.randint(1, 898)))

            self.assertEqual(response.status_code, 302)

            # Test when redirect is followed
            with captured_templates(self.app) as templates:
                response = c.post(url_for("pokemon.edit_team_slot_pokemon", team_id=team_pokemon.team_id,
                                          team_index=team_pokemon.team_index, pokeapi_id=random.randint(1, 898)), follow_redirects=True)
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "pokemon_view.html")

    def test_delete_team_slot_pokemon(self):
        """
        Tests that the delete team slot pokemon endpoint correctly redirects and renders the team view page.
        """

        # Test status code for redirect
        with self.client as c:
            team_pokemon = self.get_random_team_pokemon()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})
            response = c.post(url_for("pokemon.delete_team_slot_pokemon", team_id=team_pokemon.team_id, team_index=team_pokemon.team_index))

            self.assertEqual(response.status_code, 302)

            self.logout()

            # Test when redirect is followed
            team_pokemon = self.get_random_team_pokemon()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})
            with captured_templates(self.app) as templates:
                response = c.post(url_for("pokemon.delete_team_slot_pokemon", team_id=team_pokemon.team_id, team_index=team_pokemon.team_index),
                                  follow_redirects=True)
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "team_view.html")
                self.assertIn(bytes(team_pokemon.team.name, "utf-8"), response.data)
