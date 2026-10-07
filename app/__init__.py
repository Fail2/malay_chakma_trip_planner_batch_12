from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])

    db.init_app(app)
    # If we put this import line it will create circular dependency
    from app.trips.routes import trips_bp
    app.register_blueprint(trips_bp, url_prefix='/api/v1/trips')
    from app.travelers.routes import travelers_bp
    app.register_blueprint(travelers_bp, url_prefix='/api/v1/trips/')

    return app