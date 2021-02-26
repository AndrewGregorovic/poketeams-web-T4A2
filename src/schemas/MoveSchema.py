from marshmallow.validate import Range

from src.main import ma
from src.models.Move import Move


class MoveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Move

    move_id = ma.Integer(validate=Range(min=1, max=826))
    move_name = ma.String()


move_schema = MoveSchema()
moves_schema = MoveSchema(many=True)
