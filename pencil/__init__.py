from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from pencil.config import Config

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)

    from pencil.models.version_1 import Movie, Year, Rating, Genre, ImdbScore, MetaScore, Director, Star

    from pencil.routes.version1 import pencil

    from pencil.errors.handlers import errors

    app.register_blueprint(pencil)
    app.register_blueprint(errors)

    return app
