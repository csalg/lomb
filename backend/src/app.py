from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from flask import Flask, jsonify, request, send_from_directory, current_app
from flask_cors import CORS

from config import LANGUAGE_NAMES
from api.texts.controllers_rest_handlers import library_blueprint
from api.tracking.rest_api import tracking
from api.user.rest_api import user_blueprint

from api.data_interpretation import (
                    etl_from_scratch,
                    ensure_datapoints_have_frequency_and_languages,
                    remove_ignored_datapoints
                    )

from api.revision import (
    revise_all_lemmas,
    drill_from_book
                    )
from api.stats import stats

app = Flask(__name__)
app.register_blueprint(tracking, url_prefix='/trk')
app.register_blueprint(library_blueprint, url_prefix='/library')
app.register_blueprint(user_blueprint, url_prefix='/user')
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
    maximum_por = float(request.args.get('maximum_por'))
    return drill_from_book(username, textfile_id, maximum_por)

@app.route('/slices/stats')
@jwt_required
def stats_endpoint():
    username = get_jwt_identity()['username']
    return stats(username)

@app.route('/slices/etl_from_scratch')
@jwt_required
def etl_from_scratch_endpoint():
    etl_from_scratch()
    return 'ok'

@app.route('/slices/data.csv')
def get_dataset():
    current_app.logger.info("YO!")
    return send_from_directory('static', 'data.csv')

@app.route('/slices/add_frequency_and_support_language_to_datapoints')
def add_frequency_and_support_language_to_datapoints_endpoint():
    ensure_datapoints_have_frequency_and_languages()
    return 'ok'

@app.route('/vocabulary/revise', methods=['POST'])
@jwt_required
def revise_all_lemmas_endpoint():
    return revise_all_lemmas()

@app.route('/slices/remove_ignored_datapoints')
def remove_ignored_datapoints_endpoint():
    remove_ignored_datapoints()
    return 'ok'
