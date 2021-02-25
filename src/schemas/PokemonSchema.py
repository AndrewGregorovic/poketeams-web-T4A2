from marshmallow.validate import Range

from src.main import ma
from src.models.Pokemon import Pokemon


class PokemonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pokemon

    team_id = ma.Integer(required=True)
    team_index = ma.Integer(required=True)
    pokemon_id = ma.Integer(required=True, validate=Range(min=1, max=898))
    pokemon_name = ma.String(required=True)
    move_1_id = ma.Integer(validate=Range(min=0, max=898))
    move_1_name = ma.String()
    move_2_id = ma.Integer(validate=Range(min=0, max=898))
    move_2_name = ma.String()
    move_3_id = ma.Integer(validate=Range(min=0, max=898))
    move_3_name = ma.String()
    move_4_id = ma.Integer(validate=Range(min=0, max=898))
    move_4_name = ma.String()
    team = ma.Nested("TeamSchema", only=("id", "name", "is_private", "owner_id"))


pokemon_schema = PokemonSchema()
pokemon_many_schema = PokemonSchema(many=True)
