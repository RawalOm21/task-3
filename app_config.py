import random
from datetime import timedelta

class Config:
    SECRET_KEY = random._urandom(32)
    JWT_SECRET_KEY = random._urandom(32)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_INITIAL_TOKEN_EXPIRATION = timedelta(minutes=1)
    SQLALCHEMY_DATABASE_URI = 'books.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False