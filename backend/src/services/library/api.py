import json

from flask import Blueprint, request, send_from_directory, current_app
from flask_jwt_extended import jwt_required

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


@library_blueprint.route('/')
@jwt_required
def all():
    all = JSONEncoder().encode(list(library.all()))
    return all