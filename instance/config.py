import os


class Config(object):
    """Parent configuration class.
    source env/bin/activate
    # DATABASE_URL = 'postgresql://localhost/flask_api'
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('some-very-long-string-of-random-characters-CHANGE-TO-YOUR-LIKING')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    FLASK_APP = 'run.py'
    DATABASE_URL = 'jdbc:postgresql://localhost/flask_api:5432/postgres'


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    APP_SETTINGS = 'development'


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
