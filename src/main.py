from dotenv import load_dotenv
from flask import flash, Flask, jsonify, redirect, render_template, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import ValidationError
import requests_cache


# Load env variables and initialise packages
load_dotenv()
db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

# Initialise cache for pokeapi.co responses, responses expire after 30 days
requests_cache.install_cache(cache_name='pokeapi_cache', expire_after=2592000)


def create_app():
    """
    Factory pattern used to create instances of a Flask app

    Returns:
    An instance of the Flask app
    """

    # These need to be inside the function
    from src.commands import db_commands
    from src.controllers import registerable_controllers
    from src.models.User import get_user

    # Create the app and load default config settings
    app = Flask(__name__)
    app.config.from_object("src.default_settings.app_config")

    # Bind extensions to the app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(db_commands)
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    # Create user loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return get_user(user_id)

    # Handle unauthorized requests
    @login_manager.unauthorized_handler
    def unauthorized():
        flash("You must be logged in to view this page.")
        return redirect(url_for("auth.login"))

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return (jsonify(error.messages), 400)

    return app


def my_error_func(error_message):
    return render_template("404.html"), 404
