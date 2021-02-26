from marshmallow.validate import Range

from src.main import ma
from src.models.Pokemon import Pokemon


class PokemonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pokemon

    pokeapi_id = ma.Integer(required=True)
    pokemon_id = ma.Integer(required=True, validate=Range(min=1, max=898))
    pokemon_name = ma.String(required=True)
    pokemon_moves = ma.Nested("PokemonMovesSchema", only=("move_id", "pokemon_move_index", "move"))


pokemon_schema = PokemonSchema()
pokemon_many_schema = PokemonSchema(many=True)
