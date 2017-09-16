import os


class Config(object):
    """Parent configuration class.
    # DATABASE_URL = 'postgresql://localhost/flask_api'
      set FLASK_APP="run.py"
      set APP_SETTINGS="development"
      set SECRET="a-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING"
      set DATABASE_URL="postgresql://localhost/flask_api"
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    FLASK_APP = "run.py"
    DATABASE_URL = 'jdbc:postgresql://localhost/flask_api:5432/postgres'


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_api_db'
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
