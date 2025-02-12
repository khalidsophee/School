import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///students.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "Kh@@@lid@@@"  # Change this to a strong key
    JWT_SECRET_KEY = "Kh@@@lid@@@"  # Secret for JWT authentication
    JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = 86400  # 1 day
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = "session:"
