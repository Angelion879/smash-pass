from hashlib import sha3_256
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, UserMixin
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from .secrets import *

mongo = PyMongo()

class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
        self.username = user_data['username']
        self.id = str(user_data['_id'])

    def get_id(self):
        return self.id

    @staticmethod
    def get(user_id):
        user_data = mongo.db.users.find_one({'_id':ObjectId(user_id)})
        if user_data:
            return User(user_data)

        return None


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = app_secret,
    )
    app.config['MONGO_URI'] = mongo_uri

    mongo.init_app(app)

    login_man = LoginManager(app)
    login_man.login_view = 'login'

    @app.route('/')
    def hello():
        return render_template('index.html')

    @login_man.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            hashed = sha3_256(password.encode('utf-8')).hexdigest()

            user_data = mongo.db.users.find_one({'username': username})
            if user_data and (user_data['password'] == hashed):
                user = User(user_data)
                login_user(user)
                return redirect(url_for('dash'))
            else:
                flash('Wrong Username or Password')

        return render_template('login.html')

    @app.route('/dash')
    @login_required
    def dash():
        return f'Hello, {current_user.username}!'

    return app
