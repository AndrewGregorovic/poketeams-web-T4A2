import random

from flask import url_for

from src.models.Move import Move
from src.models.PokemonMoves import Pokemon_Moves
from tests.CustomBaseTestClass import CustomBaseTestClass


class TestMovesBackend(CustomBaseTestClass):
    """
    Test cases to test the backend logic of the moves controller endpoints.
    """

    def test_edit_pokemon_move_slot(self):
        """
        Tests that the edit pokemon move slot endpoint correctly adds or updates the move in the database.
        """

        with self.client as c:
            # Updating a move
            team_pokemon, move = self.get_move_slot_public()
            move_id = random.randint(1, 826)

            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})
            response = c.post(url_for("moves.edit_pokemon_move_slot", team_id=team_pokemon.team_id,
                                      team_index=team_pokemon.team_index, pokemon_move_index=move.pokemon_move_index,
                                      move_id=move_id), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(move.move_id, move_id)

            # Check the move exists in the database
            self.assertTrue(Move.query.get(move_id))
            self.assertTrue(Pokemon_Moves.query.get((team_pokemon.id, team_pokemon.pokeapi_id, move.pokemon_move_index)))

            # Adding a move
            team_pokemon, move_index = self.get_empty_move_slot()
            move_id = random.randint(1, 826)

            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})
            response = c.post(url_for("moves.edit_pokemon_move_slot", team_id=team_pokemon.team_id,
                                      team_index=team_pokemon.team_index, pokemon_move_index=move_index,
                                      move_id=move_id), follow_redirects=True)

            self.assertEqual(response.status_code, 200)

            # Check the new move exists in the database
            self.assertTrue(Move.query.get(move_id))
            self.assertTrue(Pokemon_Moves.query.get((team_pokemon.id, team_pokemon.pokeapi_id, move_index)))

    def test_delete_pokemon_move_slot(self):
        """
        Tests that the delete pokemon move slot endpoint correctly deletes the move from the database.
        """

        with self.client as c:
            team_pokemon, move = self.get_move_slot_public()
            self.login({"email": f"test{team_pokemon.team.owner_id}@test.com", "password": "123456"})

            response = c.post(url_for("moves.delete_pokemon_move_slot", team_id=team_pokemon.team_id,
                                      team_index=team_pokemon.team_index, pokemon_move_index=move.pokemon_move_index), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertFalse(Pokemon_Moves.query.get((team_pokemon.id, team_pokemon.pokeapi_id, move.pokemon_move_index)))
