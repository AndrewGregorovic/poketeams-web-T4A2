from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email


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
