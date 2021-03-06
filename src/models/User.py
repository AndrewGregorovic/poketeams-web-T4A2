from flask_login import UserMixin

from src.main import bcrypt, db


def get_user(user_id):
    """
    Function required for the user loader callback,
    returns a user object from a given user id.
    """

    user = User.query.filter_by(id=user_id).first()
    return user


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    teams = db.relationship("Team", backref="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"

    @classmethod
    def check_unique_email(cls, email):
        """
        Checks uniqueness of an email address, returns True if unique
        """

        if User.query.filter_by(email=email).first():
            return False
        return True

    @classmethod
    def check_unique_username(cls, username):
        """
        Checks uniqueness of a username, returns True if unique
        """

        if User.query.filter_by(username=username).first():
            return False
        return True

    def check_password(self, password):
        """
        Checks that password data entered in a form matches the password has in the database
        """

        return bcrypt.check_password_hash(self.password, password)
