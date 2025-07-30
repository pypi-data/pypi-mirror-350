import os

class Config:
    SECRET_KEY = os.environ.get('1234') or 'lol-gd-123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usr:pswd@127.0.0.1:3306/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False