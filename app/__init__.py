from environs import Env
env = Env()
env.read_env()

import os
from flask import Flask
from flask_migrate import Migrate
from .model import configure as config_db


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/Novodatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    config_db(app)

    Migrate(app, app.db)


    from .service import bp_app
    app.register_blueprint(bp_app)

    from .databaseService import bp_entregas
    app.register_blueprint(bp_entregas)

    return app
