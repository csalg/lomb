import re

from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from jsonschema import validate

from .domain.domain import UsersDomain
from .domain.models import User
from config import MINIMUM_PASSWORD_LENGTH, MAXIMUM_PASSWORD_LENGTH, SUPPORT_LANGUAGES, SOURCE_LANGUAGES

user_blueprint = Blueprint('users', __name__, template_folder='templates')
domain = UsersDomain()

login_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["username", "password"]
}

registration_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string"},
        "password": {"type": "string"},
        "learning_languages": {"type": "array"},
        "known_languages": {"type": "array"}
    },
    "required": ["username", "password", "learning_languages", "known_languages"]
}


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            validate(instance=request.json, schema=login_schema)
        except Exception as e:
            return jsonify({'error':str(e)}), 400
        username, password = request.json['username'], request.json['password']
        user = domain.authenticate_user(username, password)
        if user:
            access_token = user_to_access_token(user)
            return jsonify({'access_token': access_token})
        return jsonify({'error': 'Incorrect username or password'}), 400

    else:
        return render_template('login.html')


def user_to_access_token(user):
    username_and_role = {
        "username": user['_id'],
        "role": user['role']
    }
    return create_access_token(identity=username_and_role)

@user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            validate(instance=request.json, schema=registration_schema)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
        if domain.check_username(request.json['username']):
            return jsonify({'error': 'Username already taken'}), 400
        else:
            try:
                user = make_user_from_json(**request.json)
            except Exception as e:
                return jsonify({'error': str(e)}), 400
            domain.add_user(user)
            access_token = user_to_access_token(user.to_dict())
            return jsonify({'access_token': access_token})
    else:
        return render_template('register.html.j2')

@user_blueprint.route('/')
@jwt_required
def user():
    username = get_jwt_identity()['username']
    user = domain.get_user(username)
    del user['password']
    return user



email_validation_regex = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")


def make_user_from_json(username="", password="", learning_languages=[], known_languages=[]):
    if not username or not password or not learning_languages or not known_languages:
        raise Exception("Empty fields found. User was not created")
    if len(password) < MINIMUM_PASSWORD_LENGTH or len(password)> MAXIMUM_PASSWORD_LENGTH:
        raise Exception(f"Password must be between {MINIMUM_PASSWORD_LENGTH} and {MAXIMUM_PASSWORD_LENGTH} characters")
    for learning_language in learning_languages:
        if learning_language not in SOURCE_LANGUAGES:
                raise Exception(f"{learning_language} is not a valid target language")
    for known_language in known_languages:
        if known_language not in SUPPORT_LANGUAGES:
            raise Exception(f"{known_language} is not a valid support language")
    return User(username, password, learning_languages, known_languages, "user")
