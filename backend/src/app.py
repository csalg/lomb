from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from flask import Flask, render_template, jsonify
from flask_cors import CORS

from config import LANGUAGE_NAMES
from services.library.controllers_rest_handlers import library_blueprint
from services.tracking.rest_api import tracking
from services.user.rest_api import user_blueprint
from services.vocabulary.rest_api import vocabulary
from slices.drill_from_book import drill_from_book_slice

app = Flask(__name__)
app.register_blueprint(tracking, url_prefix='/tracking')
app.register_blueprint(library_blueprint, url_prefix='/library')
app.register_blueprint(vocabulary, url_prefix='/vocabulary')
app.register_blueprint(user_blueprint, url_prefix='/user')
# CORS(app, resources={r'*': {'origins': ['http://localhost:3000', 'http://127.0.0.1:3000']}}, supports_credentials=True)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)


@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@app.route('/langs')
@jwt_required
def langs():
    return jsonify(LANGUAGE_NAMES)

@app.route('/slices/drill_book/<textfile_id>')
@jwt_required
def drill_from_book(textfile_id):
    username = get_jwt_identity()['username']
    return drill_from_book_slice(username, textfile_id)
