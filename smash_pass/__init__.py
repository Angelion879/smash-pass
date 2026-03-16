from flask import Flask
from .secrets import *

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = app_secret,
    )

    @app.route('/')
    def hello():
        return "howdy, partner!"

    return app
