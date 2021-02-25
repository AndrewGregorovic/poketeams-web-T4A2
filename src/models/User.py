from src.main import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    teams = db.relationship("Team", backref="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"
