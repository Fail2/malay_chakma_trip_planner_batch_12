from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])

    db.init_app(app)

    return app