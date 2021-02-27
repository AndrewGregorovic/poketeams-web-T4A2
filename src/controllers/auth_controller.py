from flask import abort, Blueprint, jsonify, request
from flask_login import login_user

from src.main import bcrypt, db
from src.models.User import User
from src.schemas.UserSchema import user_schema


auth = Blueprint("auth", __name__)


# @auth.route("/", methods=["GET"])
# def landing_page():
#     pass


@auth.route("/auth/register", methods=["POST"])
def auth_register():
    user_fields = user_register_schema.load(request.json)

    if User.query.filter_by(username=user_fields["username"]).first():
        return abort(400, description="Username already in use.")
    if User.query.filter_by(email=user_fields["email"]).first():
        return abort(400, description="Email already registered.")

    user = User()
    user.username = user_fields["username"]
    user.email = user_fields["email"]
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

    db.session.add(user)
    db.session.commit()

    return (jsonify(user_schema.dump(user)), 201)


@auth.route("/login", methods=["POST"])
def auth_login():
    user_fields = user_schema.load(request.json)
    user = User.query.filter_by(email=user_fields["email"]).first()

    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect email and password.")

    login_user(user)

    return f"{user.username} logged in successfully"


# @auth.route("/logout", methods=["GET"])
# def logout():
#     pass
