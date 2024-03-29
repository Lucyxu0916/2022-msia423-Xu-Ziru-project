import os

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 5001
APP_NAME = "BodyFatCalculator"
SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100
SQLALCHEMY_TRACK_MODIFICATIONS = True

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
if SQLALCHEMY_DATABASE_URI is None:
    SQLALCHEMY_DATABASE_URI = "sqlite:///data/bodyfat.db"
