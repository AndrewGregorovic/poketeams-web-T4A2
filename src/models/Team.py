from src.main import db


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    is_private = db.Column(db.Boolean, nullable=False, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    team_pokemon = db.relationship("Teams_Pokemon", backref="team", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Team {self.id}: {self.name}>"
