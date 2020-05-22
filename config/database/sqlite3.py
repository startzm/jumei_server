from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, STATIC_URL_PATH

__all__ = ['db', 'app']

app = Flask(__name__,
            static_url_path=STATIC_URL_PATH,
            static_folder='../../static',
            template_folder='../../templates'
            )


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)