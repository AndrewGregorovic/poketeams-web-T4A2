from marshmallow.validate import Range

from src.main import ma
from src.models.PokemonMoves import Pokemon_Moves


class PokemonMovesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pokemon_Moves

    pokeapi_id = ma.Integer(required=True, validate=Range(min=1, max=898))
    pokemon_move_index = ma.Integer(required=True, validate=Range(min=1, max=4))
    move_id = ma.Integer(required=True, validate=Range(min=1, max=826))
    move = ma.Nested("MoveSchema", only=("move_name",))


pokemon_move_schema = PokemonMovesSchema()
pokemon_moves_schema = PokemonMovesSchema(many=True)
