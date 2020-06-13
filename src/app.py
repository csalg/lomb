from flask_jwt_extended import JWTManager

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from services.library.http_controllers import library
from services.tracking.rest_controllers import tracking
from services.users.http_controllers import users
from services.vocabulary.http_controllers import vocabulary

app = Flask(__name__)
app.register_blueprint(tracking, url_prefix='/tracking')
app.register_blueprint(library, url_prefix='/library')
app.register_blueprint(vocabulary, url_prefix='/vocabulary')
app.register_blueprint(users, url_prefix='/users')
CORS(app, resources=r'*')

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)


@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@app.route('/')
def index():
    return render_template('index.html.j2')
