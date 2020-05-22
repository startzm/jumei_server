from flask_login import UserMixin

from config.database import db

__all__ = ['Admin']


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    username = db.Column(db.String(32))
    password = db.Column(db.String(100))
    phoneNum = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(120), unique=True)
    store_name = db.Column(db.String(32))
    store_id = db.Column(db.String(32))
    header = db.Column(db.String(256))
    token = db.Column(db.String(50), unique=True)
    is_super = db.Column(db.Boolean, default=False)

    def __init__(self, username, phoneNum, password):
        self.username = username
        self.phoneNum = phoneNum
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.phoneNum