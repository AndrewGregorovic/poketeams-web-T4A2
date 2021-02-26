from src.main import db


class Pokemon_Moves(db.Model):
    __tablename__ = "pokemon_moves"

    team_pokemon_id = db.Column(db.Integer, db.ForeignKey("teams_pokemon.id"), primary_key=True)
    pokeapi_id = db.Column(db.Integer, db.ForeignKey("pokemon.pokeapi_id"), primary_key=True)
    pokemon_move_index = db.Column(db.Integer, primary_key=True)
    move_id = db.Column(db.Integer, db.ForeignKey("moves.move_id"))
    move = db.relationship("Move")

    def __repr__(self):
        return f"<Pokemon #{self.pokeapi_id}, Slot {self.pokemon_move_index}>"
