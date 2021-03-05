from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, logout_user

from src.forms import DeleteUserAccountForm, EditUserAccountForm
from src.main import bcrypt, db
from src.models.User import User
from src.schemas.UserSchema import user_schema


users = Blueprint("users", __name__)


@users.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html")


@users.route("/account", methods=["GET"])
@login_required
def get_user_account_details():
    form = DeleteUserAccountForm()
    return render_template("account.html", form=form)


@users.route("/account/edit", methods=["GET", "POST"])
@login_required
def edit_user_account_details():

    form = EditUserAccountForm()
    if form.validate_on_submit():
        if current_user.username != form.username.data and not User.check_unique_username(form.username.data):
            flash("A user already exists with that username.")
        elif current_user.email != form.email.data and not User.check_unique_email(form.email.data):
            flash("A user already exists with that email address.")
        elif form.new_password.data and not current_user.check_password(form.current_password.data):
            flash("Your current password is incorrect.")
        else:
            user = User.query.filter_by(id=current_user.id)

            data = {}
            if form.username.data:
                data["username"] = form.username.data
            if form.email.data:
                data["email"] = form.email.data
            if form.confirm_password.data:
                data["password"] = bcrypt.generate_password_hash(form.confirm_password.data).decode("utf-8")

            fields = user_schema.load(data, partial=True)

            user.update(fields)
            db.session.commit()

            flash("Account details updated successfully.")
            return redirect(url_for("users.get_user_account_details"))

    return render_template("account_edit.html", form=form)


@users.route("/account/delete", methods=["POST"])
@login_required
def delete_user_account():
    form = DeleteUserAccountForm()
    if form.validate_on_submit():
        user = current_user

        db.session.delete(user)
        db.session.commit()

        logout_user()
        flash("User successfully deleted.")

        return redirect(url_for("auth.landing_page"))
