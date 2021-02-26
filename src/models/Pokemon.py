from src.main import db


class Pokemon(db.Model):
    __tablename__ = "pokemon"

    pokeapi_id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, nullable=False)
    pokemon_name = db.Column(db.String(), nullable=False)
    pokemon_moves = db.relationship("Pokemon_Moves", backref="pokemon", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<{self.pokeapi_id} (#{self.pokemon_id} {self.pokemon_name})>"
