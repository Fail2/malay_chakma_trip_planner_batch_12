from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    # If we put this import line it will create circular dependency
    from app.routes import trips_bp
    app.register_blueprint(trips_bp, url_prefix='/api/v1/trips')

    return app