from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from src.forms import LogInForm, SignUpForm
from src.main import bcrypt, db
from src.models.User import User


auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET"])
def landing_page():
    return render_template("landing.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():

    form = SignUpForm()
    if form.validate_on_submit():
        if User.check_unique_username(form.username.data):
            flash("A user already exists with that username.")
        elif User.check_unique_email(form.email.data):
            flash("A user already exists with that email address.")
        else:
            user = User()
            user.username = form.username.data
            user.email = form.email.data
            user.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

            db.session.add(user)
            db.session.commit()

            login_user(user)

            """Need to change this redirect after coding the users controller"""
            return redirect(url_for("auth.landing_page"))

    return render_template("signup.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("auth.landing_page"))
        else:
            flash("Invalid email and password.")
            return redirect(url_for("auth.login"))

    return render_template("login.html", form=form)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.landing_page"))
