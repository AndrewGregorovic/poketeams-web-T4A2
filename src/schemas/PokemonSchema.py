from marshmallow.validate import OneOf, Range

from src.main import ma
from src.models.Pokemon import Pokemon


class PokemonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pokemon

    pokeapi_id = ma.Integer(required=True, validate=OneOf({*range(1, 899), *range(10001, 10221)}))
    pokemon_id = ma.Integer(required=True, validate=Range(min=1, max=898))
    pokemon_name = ma.String(required=True)


pokemon_schema = PokemonSchema()
pokemon_many_schema = PokemonSchema(many=True)
