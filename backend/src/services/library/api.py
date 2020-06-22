import json

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from services.library.domain import Library

library_blueprint = Blueprint('library', __name__, template_folder='templates')
library = Library()


@library_blueprint.route('/upload', methods=['POST'])
@jwt_required
def upload():
    uploaded_file = request.files['file']
    response_msg = ""
    try:
        library.add(uploaded_file.stream)
    except Exception as e:
        response_msg += str(e) + '\n'
    return response_msg if response_msg else str(request.files)

@library_blueprint.route('/')
@jwt_required
def all():
    return json.dumps(list(library.all()))
