import random

from flask import url_for

from src.forms import ConfirmForm, RemoveMoveForm
from src.models.PokemonMoves import Pokemon_Moves
from src.models.TeamsPokemon import Teams_Pokemon
from tests.CustomBaseTestClass import CustomBaseTestClass
from tests.helper_function import captured_templates


class TestMovesFrontend(CustomBaseTestClass):
    """
    Test cases to test the frontend template rendering and redirects of the pokemon controller endpoints.
    """

    def test_view_pokemon_move(self):
        """
        Tests that the move view page is rendered correctly.
        """

        with self.client as c:

            # Test the view of a pokemon's move on a users team
            move = random.choice(Pokemon_Moves.query.all())
            team_pokemon = Teams_Pokemon.query.filter_by(id=move.team_pokemon_id).first()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("moves.view_pokemon_move", team_id=team_pokemon.team_id,
                                         team_index=team_pokemon.team_index, pokemon_move_index=move.pokemon_move_index))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "move_view.html")
                self.assertIsInstance(context["form"], RemoveMoveForm)
                self.assertIn(b"Change Move", response.data)
                self.assertIn(b"Remove Move", response.data)
                self.assertIn(bytes(team_pokemon.team.name, "utf-8"), response.data)

            self.logout()

            # Test the view move endpoint redirects to the move_list template when trying to view an empty move slot
            team_pokemon, move_index = self.get_empty_move_slot()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})

            response = c.get(url_for("moves.view_pokemon_move", team_id=team_pokemon.team_id,
                                     team_index=team_pokemon.team_index, pokemon_move_index=move_index))

            self.assertEqual(response.status_code, 302)

            with captured_templates(self.app) as templates:
                response = c.get(url_for("moves.view_pokemon_move", team_id=team_pokemon.team_id,
                                         team_index=team_pokemon.team_index, pokemon_move_index=move_index), follow_redirects=True)
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "move_select.html")

            self.logout()

            # Test the view of a pokemon's move in a public team by another user or with anonymous user
            team_pokemon, move = self.get_move_slot_public()

            with captured_templates(self.app) as templates:
                response = c.get(url_for("moves.view_pokemon_move", team_id=team_pokemon.team_id,
                                         team_index=team_pokemon.team_index, pokemon_move_index=move.pokemon_move_index))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "move_view.html")
                self.assertNotIn(b"Change Move", response.data)
                self.assertNotIn(b"Remove Move", response.data)
                self.assertIn(bytes(team_pokemon.team.name, "utf-8"), response.data)

    def test_get_pokemon_move_list(self):
        """
        Tests that the move list page is rendered correctly.
        """

        with self.client as c:
            team_pokemon = self.get_random_team_pokemon()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("moves.get_pokemon_move_list", team_id=team_pokemon.team_id,
                                         team_index=team_pokemon.team_index, pokemon_move_index=random.randint(1, 4)))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "move_select.html")
                self.assertIn(bytes(team_pokemon.team.name, "utf-8"), response.data)
                self.assertIn(bytes(team_pokemon.pokemon.pokemon_name, "utf-8"), response.data)

    def test_view_selected_pokemon_move(self):
        """
        Tests that the move view page for the selected move is rendered correctly.
        """

        with self.client as c:
            team_pokemon = self.get_random_team_pokemon()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})

            with captured_templates(self.app) as templates:
                response = c.get(url_for("moves.view_selected_pokemon_move", team_id=team_pokemon.team_id,
                                         team_index=team_pokemon.team_index, pokemon_move_index=random.randint(1, 4),
                                         move_id=random.randint(1, 826)))
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "move_view.html")
                self.assertIsInstance(context["form"], ConfirmForm)
                self.assertIn(b"Confirm", response.data)
                self.assertIn(bytes(team_pokemon.team.name, "utf-8"), response.data)

    def test_edit_pokemon_move_slot(self):
        """
        Tests that the edit pokemon move slot endpoint correctly redirects on confirming a move change and renders the pokemon view page for that pokemon.
        """

        # Test status code for redirect
        with self.client as c:
            team_pokemon = self.get_random_team_pokemon()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})
            response = c.post(url_for("moves.edit_pokemon_move_slot", team_id=team_pokemon.team_id,
                                      team_index=team_pokemon.team_index, pokemon_move_index=random.randint(1, 4),
                                      move_id=random.randint(1, 826)))

            self.assertEqual(response.status_code, 302)

            # Test when redirect is followed
            with captured_templates(self.app) as templates:
                response = c.post(url_for("moves.edit_pokemon_move_slot", team_id=team_pokemon.team_id,
                                  team_index=team_pokemon.team_index, pokemon_move_index=random.randint(1, 4),
                                  move_id=random.randint(1, 826)), follow_redirects=True)
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "pokemon_view.html")

    def test_delete_pokemon_move_slot(self):
        """
        Tests that the delete pokemon move slot endpoint correctly redirects and renders the pokemon view page.
        """

        # Test status code for redirect
        with self.client as c:
            move = random.choice(Pokemon_Moves.query.all())
            team_pokemon = Teams_Pokemon.query.filter_by(id=move.team_pokemon_id).first()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})
            response = c.post(url_for("moves.delete_pokemon_move_slot", team_id=team_pokemon.team_id,
                                      team_index=team_pokemon.team_index, pokemon_move_index=move.pokemon_move_index))

            self.assertEqual(response.status_code, 302)

            self.logout()

            # Test when redirect is followed
            move = random.choice(Pokemon_Moves.query.all())
            team_pokemon = Teams_Pokemon.query.filter_by(id=move.team_pokemon_id).first()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})
            with captured_templates(self.app) as templates:
                response = c.post(url_for("moves.delete_pokemon_move_slot", team_id=team_pokemon.team_id,
                                          team_index=team_pokemon.team_index, pokemon_move_index=move.pokemon_move_index), follow_redirects=True)
                template, context = templates[0]

                self.assertEqual(response.status_code, 200)
                self.assertEqual(template.name, "pokemon_view.html")
