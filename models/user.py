from flask_login import UserMixin

from config.database import db

__all__ = ['User']


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(100))
    phoneNum = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(120), unique=True)
    gender = db.Column(db.String(10))
    birth = db.Column(db.String(100))
    header = db.Column(db.String(256))
    region = db.Column(db.String(64))
    slogon = db.Column(db.String(32))
    discount = db.Column(db.String(32))
    token = db.Column(db.String(50), unique=True)

    def __init__(self, username, phoneNum):
        self.phoneNum = username
        self.phoneNum = phoneNum

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.phoneNum