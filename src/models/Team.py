from src.main import db


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(2000), nullable=True)
    is_private = db.Column(db.Boolean, nullable=False, default=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    team_pokemon = db.relationship("Teams_Pokemon", backref="team", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Team {self.id}: {self.name}>"

    @staticmethod
    def sort_team_pokemon(teams):
        """
        Sorts pokemon in team.team_pokemon by team index for a list of teams
        """

        if type(teams) == list:
            for team in teams:
                team.team_pokemon.sort(key=lambda x: x.team_index)
            return teams

    @staticmethod
    def fill_empty_team_slots(team_list_dict):
        """
        Takes a list of team dicts and fills empty pokemon slots with None
        """

        for team in team_list_dict:
            indices = [pokemon["team_index"] for pokemon in team["team_pokemon"]]
            for i in range(6):
                if i + 1 not in indices:
                    team["team_pokemon"].insert(i, None)
        return team_list_dict
