from flask_jwt_extended import JWTManager, jwt_required

from flask import Flask, render_template, jsonify
from flask_cors import CORS

from config import LANGUAGE_NAMES
from services.library.api import library_blueprint
from services.tracking.rest_controllers import tracking
from services.user.rest_controllers import user_blueprint
from services.vocabulary.rest_controllers import vocabulary

app = Flask(__name__)
app.register_blueprint(tracking, url_prefix='/tracking')
app.register_blueprint(library_blueprint, url_prefix='/library')
app.register_blueprint(vocabulary, url_prefix='/vocabulary')
app.register_blueprint(user_blueprint, url_prefix='/user')
CORS(app, resources=r'*')

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)


@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@app.route('/')
def index():
    return render_template('index.html.j2')

@app.route('/langs')
@jwt_required
def langs():
    return jsonify(LANGUAGE_NAMES)
