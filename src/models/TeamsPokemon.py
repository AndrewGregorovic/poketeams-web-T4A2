from src.main import db


class Teams_Pokemon(db.Model):
    __tablename__ = "teams_pokemon"

    id = db.Column(db.Integer, db.Sequence("teams_pokemon_id_seq"), unique=True, autoincrement=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), primary_key=True)
    team_index = db.Column(db.Integer, primary_key=True)
    pokeapi_id = db.Column(db.Integer, db.ForeignKey("pokemon.pokeapi_id"))
    pokemon = db.relationship("Pokemon")
    pokemon_moves = db.relationship("Pokemon_Moves", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Team {self.team_id}, Slot {self.team_index}>"
