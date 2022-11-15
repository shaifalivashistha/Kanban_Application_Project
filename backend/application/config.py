import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False

    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"

    CACHE_TYPE = "RedisCache"
    REDIS_URL = "redis://localhost:6379"
    CACHE_REDIS_URL = "redis://localhost:6379/0"

    ENABLE_UTC = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"


class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///kanbandb.sqlite3"

    DEBUG = True
    SECRET_KEY = "Th1s1sas3cr3tk3y"
    SECURITY_PASSWORD_SALT = "S3cr3tPassword"  # Read from ENV in your case
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    WTF_CSRF_ENABLED = False

    SMTP_SERVER_HOST = "localhost"
    SMTP_SERVER_PORT = 1025
    SENDER_ADDRESS = "admin@kanbanTodo.com"
    SENDER_PASSWORD = ""

    CACHE_TYPE = "RedisCache"
    REDIS_URL = "redis://localhost:6379"
    CACHE_REDIS_URL = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 1800
    CACHE_KEY_PREFIX = "kanbanToDo"

    ENABLE_UTC = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
