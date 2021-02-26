from marshmallow.validate import Length

from src.main import ma
from src.models.Team import Team


class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team

    name = ma.String(required=True, validate=Length(max=30))
    description = ma.String(validate=Length(max=255))
    is_private = ma.Boolean()
    owner_id = ma.Integer(required=True)
    team_pokemon = ma.Nested("TeamsPokemonSchema", many=True, only=("team_index", "pokemon_id", "pokemon"))


team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
