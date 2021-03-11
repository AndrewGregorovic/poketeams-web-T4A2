import json
import requests

from src.main import db


class Move(db.Model):
    __tablename__ = "moves"

    move_id = db.Column(db.Integer, primary_key=True)
    move_name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<(#{self.move_id} {self.move_name})>"

    @staticmethod
    def get_move_data(move_id):
        return json.loads(requests.get(f"https://pokeapi.co/api/v2/move/{move_id}").text)

    @staticmethod
    def get_move_list(pokemon_data, move_set):
        learned_moves = {move.move.move_name for move in move_set}
        return [[move["move"]["name"], move["move"]["url"].replace("https://pokeapi.co/api/v2/move/", "").replace("/", "")]
                for move in pokemon_data["moves"] if move["move"]["name"] not in learned_moves]
