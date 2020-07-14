import json

from flask import Blueprint, request, send_from_directory, current_app, jsonify
from flask_jwt_extended import jwt_required
from jsonschema import validate

from mq.signals import new_word_to_learn_was_added
from services.library.domain import Library
from config import UPLOADS_FOLDER
from lib.json import JSONEncoder
from services.library.signals import new_lemma_was_added_handler

library_blueprint = Blueprint('library', __name__, template_folder='templates')
library = Library()
new_word_to_learn_was_added.connect(new_lemma_was_added_handler)



@library_blueprint.route('/upload', methods=['POST'])
@jwt_required
def upload():
    uploaded_file = request.files['file']
    response_msg = ""
    try:
        response_msg += library.add(uploaded_file)
    except Exception as e:
        response_msg += str(e) + '\n'
        current_app.logger.info(e)
    return response_msg if response_msg else str(request.files)


@library_blueprint.route('/uploads/<filename>')
@jwt_required
def uploaded_text(filename):
    return send_from_directory(UPLOADS_FOLDER, filename)


text_request_schema = {
    "type": "object",
    "properties": {
        "learning_languages": {"type": "array"},
        "known_languages": {"type": "array"}
    },
    "required": ["learning_languages", "known_languages"]
}



@library_blueprint.route('/', methods=['POST'])
@jwt_required
def all():
    current_app.logger.info(request)
    current_app.logger.info('All textfiles endpoint')
    try:
        validate(instance=request.json, schema=text_request_schema)
    except Exception as e:
        current_app.logger.info(str(e))
        return jsonify({'error': str(e)}), 400

    learning_languages, known_languages = request.json['learning_languages'], request.json['known_languages']
    all = JSONEncoder().encode(list(library.all_filtered_by_language(learning_languages,known_languages)))
    current_app.logger.info(all)
    return all
