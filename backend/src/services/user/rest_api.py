from flask import Blueprint, render_template, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from .db import CredentialsRepository, UserPreferencesRepository
from .domain.credentials import CredentialsDTO, CredentialsWriteModel, CredentialsReadModel
from .rest_controllers_lib import CredentialsParser, RegistrationJsonValidator


user_blueprint = Blueprint('users', __name__, template_folder='templates')
credentials_repository = CredentialsRepository()
user_preferences_repository = UserPreferencesRepository()


@user_blueprint.route('/login', methods=['POST'])
def login(credentials_parser=CredentialsParser, credentials_repository=credentials_repository):
    try:
        credentials_dto = credentials_parser.from_json(request.json)
        credentials: CredentialsReadModel = credentials_repository.find(credentials_dto)
        access_token = create_access_token(identity=credentials)
        return jsonify({'access_token': access_token})
    except Exception as e:
        return jsonify({'error':str(e)}), 400


@user_blueprint.route('/register', methods=['POST'])
def register():
    try:
        credentials_write_model, preferences = RegistrationJsonValidator.from_json(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    if credentials_repository.check(credentials_write_model.username):
        return jsonify({'error': 'Username already taken'}), 400
    else:
        try:
            credentials_repository.add(credentials_write_model.to_dict())
            user_preferences_repository.add(preferences.to_dict())
            credentials_read_model = credentials_write_model.to_read_model()
            access_token = create_access_token(identity=credentials_read_model.to_dict())
            current_app.logger.info('Successfully added')
            return jsonify({'access_token': access_token})
        except Exception as e:
            current_app.logger.info(e)
            return jsonify({'error': str(e)}), 400


@user_blueprint.route('/')
@jwt_required
def user_preferences():
    try:
        username = get_jwt_identity()['username']
        current_app.logger.info(username)
        user_preferences = user_preferences_repository.find(username)
        return user_preferences
    except Exception as e:
        current_app.logger.info(e)
        return jsonify({'error':str(e)}), 400
