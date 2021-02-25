from src.main import db


class Pokemon(db.Model):
    __tablename__ = "pokemon"

    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), primary_key=True)
    team_index = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, nullable=False)
    pokemon_name = db.Column(db.String, nullable=False)
    move_1_id = db.Column(db.Integer, nullable=False, default=0)
    move_1_name = db.Column(db.String, nullable=True)
    move_2_id = db.Column(db.Integer, nullable=False, default=0)
    move_2_name = db.Column(db.String, nullable=True)
    move_3_id = db.Column(db.Integer, nullable=False, default=0)
    move_3_name = db.Column(db.String, nullable=True)
    move_4_id = db.Column(db.Integer, nullable=False, default=0)
    move_4_name = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Team {self.team_id}, Slot {self.team_index}: #{self.pokemon_id} {self.pokemon_name}>"
