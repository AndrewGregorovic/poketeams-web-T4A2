import json
import requests

from src.main import db


class Pokemon(db.Model):
    __tablename__ = "pokemon"

    pokeapi_id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, nullable=False)
    pokemon_name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<{self.pokeapi_id} (#{self.pokemon_id} {self.pokemon_name})>"

    @staticmethod
    def get_pokedex_list():
        return json.loads(requests.get("https://pokeapi.co/api/v2/pokemon?limit=898&offset=0").text)

    @staticmethod
    def get_pokemon_data(pokeapi_id):
        return json.loads(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokeapi_id}").text)

    @staticmethod
    def get_pokemon_ability_data(ability_url):
        return json.loads(requests.get(ability_url).text)
