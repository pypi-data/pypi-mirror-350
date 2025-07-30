from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

db = SQLAlchemy()

def init_db(app):
    with app.app_context():
        db.init_app(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    password_hash = db.Column(db.String(256))
    role = db.Column(Enum("user", "admin"))
