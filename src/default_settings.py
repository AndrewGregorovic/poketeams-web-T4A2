import os


def get_env_var(env_var):
    """
    Utility function that fetches the requested environment variable,
    raises an error if not found.
    """

    value = os.environ.get(env_var)

    if not value:
        raise ValueError(f"{env_var} is not set")

    return value


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "poketeams_flask_login"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return get_env_var("DB_URI")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    @property
    def SECRET_KEY(self):
        return get_env_var("SECRET_KEY")


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return get_env_var("DB_TEST_URI")


class WorkflowConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return get_env_var("DB_TEST_URI")


environment = get_env_var("FLASK_ENV")

if environment == "production":
    app_config = ProductionConfig()
elif environment == "testing":
    app_config = TestingConfig()
elif environment == "workflow":
    app_config = WorkflowConfig()
else:
    app_config = DevelopmentConfig()
