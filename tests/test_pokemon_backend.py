import random

from flask import url_for

from src.models.Pokemon import Pokemon
from src.models.PokemonMoves import Pokemon_Moves
from src.models.TeamsPokemon import Teams_Pokemon
from tests.CustomBaseTestClass import CustomBaseTestClass
from tests.helper_function import captured_templates


class TestPokemonBackend(CustomBaseTestClass):
    """
    Test cases to test the backend logic of the teams controller endpoints.
    """

    def test_view_team_pokemon(self):
        """
        Tests that the logic for populating empty move slots is correctly returning data with the correct size.
        """

        with self.client as c:
            team_pokemon = self.get_random_team_pokemon_public()

            with captured_templates(self.app) as templates:
                c.get(url_for("pokemon.view_team_pokemon", team_id=team_pokemon.team_id, team_index=team_pokemon.team_index))
                template, context = templates[0]

                if context["moves"]:
                    self.assertEqual(len(context["moves"]), 4)

    def test_edit_team_slot_pokemon(self):
        """
        Tests that the edit team slot pokemon endpoint correctly adds or updates the pokemon in the database.
        """

        with self.client as c:
            # Updating a pokemon
            team_pokemon = self.get_random_team_pokemon()
            pokeapi_id = random.randint(1, 898)
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})

            response = c.post(url_for("pokemon.edit_team_slot_pokemon", team_id=team_pokemon.team_id,
                                      team_index=team_pokemon.team_index, pokeapi_id=pokeapi_id), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(team_pokemon.pokeapi_id, pokeapi_id)

            # Check the pokemon exists in the database
            self.assertTrue(Pokemon.query.get(pokeapi_id))
            self.assertTrue(Teams_Pokemon.query.get((team_pokemon.team_id, team_pokemon.team_index)))

            # Check moves assigned to the previous pokemon are deleted
            self.assertEqual(Pokemon_Moves.query.filter_by(team_pokemon_id=team_pokemon.id).all(), [])

            # Adding a pokemon
            team, team_index = self.get_empty_pokemon_slot()
            pokeapi_id = random.randint(1, 898)
            self.login({"email": f"test{team.owner_id}@test.com", "password": "123456"})

            response = c.post(url_for("pokemon.edit_team_slot_pokemon", team_id=team.id, team_index=team_index,
                                      pokeapi_id=pokeapi_id), follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            # Check the new pokemon exists in the database
            self.assertTrue(Pokemon.query.get(pokeapi_id))
            self.assertTrue(Teams_Pokemon.query.get((team.id, team_index)))

    def test_delete_team_slot_pokemon(self):
        """
        Tests that the delete team slot pokemon endpoint correctly deletes the pokemon and its assigned moves from the database.
        """

        with self.client as c:
            team_pokemon = self.get_random_team_pokemon()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})

            response = c.post(url_for("pokemon.delete_team_slot_pokemon", team_id=team_pokemon.team_id,
                                      team_index=team_pokemon.team_index), follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            # Check teams_pokemon database entry was deleted
            self.assertFalse(Teams_Pokemon.query.get((team_pokemon.team_id, team_pokemon.team_index)))

            # Check child pokemon_moves database entries were deleted
            self.assertEqual(Pokemon_Moves.query.filter_by(team_pokemon_id=team_pokemon.id).all(), [])
