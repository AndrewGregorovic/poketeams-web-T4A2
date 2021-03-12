from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from src.forms import LogInForm, SignUpForm
from src.main import bcrypt, db
from src.models.User import User


auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET"])
def landing_page():
    """
    Return the template for the landing page.
    """

    return render_template("landing.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    GET returns the template for the signup page, when the form is submitted the data is sent back
    to the endpoint using POST which creates a new user.
    """

    form = SignUpForm()
    if form.validate_on_submit():
        if not User.check_unique_username(form.username.data):
            flash("A user already exists with that username.")
        elif not User.check_unique_email(form.email.data):
            flash("A user already exists with that email address.")
        else:
            user = User()
            user.username = form.username.data
            user.email = form.email.data
            user.password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

            db.session.add(user)
            db.session.commit()

            login_user(user)

            return redirect(url_for("users.dashboard"))

    return render_template("signup.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    GET returns the template for the login page, when the form is submitted the data is sent back
    to the endpoint using POST which logs in the user.
    """

    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("users.dashboard"))
        else:
            flash("Invalid email and password.")
            return redirect(url_for("auth.login"))

    return render_template("login.html", form=form)


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    Logs out the current user by ending their session,
    uses GET as there is no form to submit to use a POST request.
    """

    logout_user()
    flash("You have been successfully logged out.")
    return redirect(url_for("auth.landing_page"))
