from flask import Flask, render_template
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

    @app.route('/login')
    def login():
        return render_template('login.html')

    return app
