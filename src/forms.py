from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=3, max=30)
    ])
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password", validators=[
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
    username = StringField("Username", validators=[
        Optional(),
        Length(min=3, max=30)
    ])
    email = StringField("Email", validators=[
        Optional(),
        Email()
    ])
    current_password = PasswordField("Current Password", validators=[
        Optional()
    ])
    new_password = PasswordField("New Password", validators=[
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
    team_name = StringField("Team Name", validators=[
        DataRequired(),
        Length(min=3, max=50)
    ])
    description = TextAreaField("description", validators=[
        Optional(),
        Length(max=255)
    ])
    is_private = BooleanField()
    submit = SubmitField("Create Team")


class EditTeamForm(FlaskForm):
    team_name = StringField("Team Name", validators=[
        Optional(),
        Length(min=3, max=50)
    ])
    description = TextAreaField("description", validators=[
        Optional(),
        Length(max=255)
    ])
    is_private = BooleanField()
    submit = SubmitField("Create Team")


class DeleteTeamForm(FlaskForm):
    submit = SubmitField("Delete Team")
