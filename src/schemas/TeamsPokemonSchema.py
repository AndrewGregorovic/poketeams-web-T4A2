from marshmallow.validate import Range

from src.main import ma
from src.models.TeamsPokemon import Teams_Pokemon


class TeamsPokemonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Teams_Pokemon

    team_id = ma.Integer(required=True)
    team_index = ma.Integer(required=True, validate=Range(min=1, max=6))
    pokemon_id = ma.Integer(required=True, validate=Range(min=1, max=898))
    pokemon = ma.Nested("PokemonSchema", only=("pokeapi_id", "pokemon_id", "pokemon_name"))


teams_pokemon_schema = TeamsPokemonSchema()
teams_pokemon_many_schema = TeamsPokemonSchema(many=True)
