from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


def strip_whitespace(string):
    if isinstance(string, str):
        string = string.strip()
    return string


class SignUpForm(FlaskForm):
    username = StringField("Username", filters=[strip_whitespace], validators=[
        DataRequired(),
        Length(min=3, max=30)
    ])
    email = StringField("Email", filters=[strip_whitespace], validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password", filters=[strip_whitespace], validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password", message="Both passwords need to match.")
    ])
    submit = SubmitField("Create Account")


class LogInForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class EditUserAccountForm(FlaskForm):
    username = StringField("Username", filters=[strip_whitespace], validators=[
        Optional(),
        Length(min=3, max=30)
    ])
    email = StringField("Email", filters=[strip_whitespace], validators=[
        Optional(),
        Email()
    ])
    current_password = PasswordField("Current Password", validators=[
        Optional()
    ])
    new_password = PasswordField("New Password", filters=[strip_whitespace], validators=[
        Optional(),
        Length(min=6)
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        EqualTo("new_password", message="Both passwords need to match.")
    ])
    submit = SubmitField("Apply Changes")


class DeleteUserAccountForm(FlaskForm):
    submit = SubmitField("Delete Account")


class CreateTeamForm(FlaskForm):
    team_name = StringField("Team Name", filters=[strip_whitespace], validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    description = TextAreaField("description", filters=[strip_whitespace], validators=[
        Optional(),
        Length(max=2000)
    ])
    is_private = BooleanField()
    submit = SubmitField("Create Team")


class EditTeamForm(FlaskForm):
    team_name = StringField("Team Name", filters=[strip_whitespace], validators=[
        Optional(),
        Length(min=3, max=50)
    ])
    description = TextAreaField("description", filters=[strip_whitespace], validators=[
        Optional(),
        Length(max=2000)
    ])
    is_private = BooleanField()
    submit = SubmitField("Apply Changes")


class DeleteTeamForm(FlaskForm):
    submit = SubmitField("Delete Team")


class ConfirmForm(FlaskForm):
    submit = SubmitField("Confirm")


class RemovePokemonForm(FlaskForm):
    submit = SubmitField("Remove Pokemon")
