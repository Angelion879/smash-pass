import requests
from hashlib import sha3_256
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, UserMixin
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from .secrets import *

poke_api = 'https://pokeapi.co/api/v2/pokemon/'
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

    @app.route('/poke/<poke_id>')
    def poke(poke_id):
        try:
            res = requests.get(poke_api+f'{poke_id}')
            if res.status_code == 200:
                data = res.json()
                exp = data['base_experience']
                age_calc = f"{(exp * (3.5 if exp <= 120 else 1.8) // 12):.0f}"
                poke_data = {
                    'profile_pic' : data['sprites']['other']['official-artwork']['front_default'],
                    'name' : data['name'],
                    'age' : age_calc,
                    'height' : f"{(data['height']*0.1):.1f}",
                    'type_list' : [i['type']['name'] for i in data['types']],
                }
                return render_template('poke_profile.html', api_data=poke_data)
        except requests.exceptions.RequestException as e:
            print(e)
            return "Something went wrong! Try again later!"

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
