from flask import Blueprint, request, send_from_directory, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from jsonschema import validate


from lib.db import get_db
from mq.signals import NewLemmaToLearnEvent
from config import UPLOADS_FOLDER
from lib.json import JSONEncoder
from bounded_contexts.library.controllers import Controllers, AddTextMetadataDTO, create_controllers_with_mongo_repositories
from bounded_contexts.library.domain.entities import UserCredentials
from bounded_contexts.library.event_handlers import new_lemma_was_added_handler
import bounded_contexts.library.controllers_rest_lib as lib

library_blueprint = Blueprint('library', __name__, template_folder='templates')
# new_lemma_to_learn_was_added.connect(new_lemma_was_added_handler)
NewLemmaToLearnEvent.addEventListener(new_lemma_was_added_handler)

db = get_db()
controllers = create_controllers_with_mongo_repositories(db)

@library_blueprint.route('/upload', methods=['POST'])
@jwt_required
def upload():
    uploaded_file = request.files['file']
    form = request.form
    username = lib.get_username()
    try:
        tags = parse_tags(form['tags'])
        current_app.logger.info(form)
        add_text_dto = AddTextMetadataDTO(username, form['title'], form['source_language'], form['support_language'], tags, form['permission'])
        extension = uploaded_file.filename.rsplit('.', 1)[1].lower()
        message = controllers.add_text(add_text_dto, uploaded_file, extension)
        return message, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def parse_tags(tags):
    if not tags:
        return []
    if ',' not in tags:
        return [tags,]
    return tags.split(',')

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
    try:
        validate(instance=request.json, schema=text_request_schema)
    except Exception as e:
        return str(e), 400

    username = lib.get_username()
    learning_languages, known_languages = request.json['learning_languages'], request.json['known_languages']
    all = JSONEncoder().encode(controllers.all_filtered_by_language(username,learning_languages,known_languages))
    return all

@library_blueprint.route('/text/<id>', methods=['DELETE'])
@jwt_required
def delete(id):
    credentials = lib.get_credentials()
    try:
        controllers.delete_text(credentials, id)
        return f'deleted {id}', 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@library_blueprint.route('/admin/update_lemma_ranks', methods=['GET'])
@jwt_required
def update_lemma_ranks():
    try:
        controllers.update_language_lemma_ranks()
        return 'Lemma ranks were successfully updated'
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@library_blueprint.route('/admin/update_text_difficulty', methods=['GET'])
@jwt_required
def update_text_difficulty():
    try:
        controllers.update_text_average_lemma_rank()
        return 'Text difficulties were successfully updated'
    except Exception as e:
        return jsonify({'error': str(e)}), 400

