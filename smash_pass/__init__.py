from flask import Flask, render_template, request, current_app
# from . import db
from flask_pymongo import PyMongo
from .secrets import *

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = app_secret,
    )
    app.config['MONGO_URI'] = mongo_uri

    mongo.init_app(app)

    @app.route('/')
    def hello():
        return render_template('index.html')


    return app
