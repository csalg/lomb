
from flask import Blueprint, render_template, request, current_app
from flask.json import JSONEncoder, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.vocabulary.infrastructure.signals import lemma_examples_were_found_handler
from .db_repository import LemmaExamplesRepository
from .domain import VocabularyDomain
from mq.signals import lemma_examples_were_found

vocabulary = Blueprint('vocabulary', __name__, template_folder='templates')
domain = VocabularyDomain()
lemma_examples_were_found.connect(lemma_examples_were_found_handler)
repository = LemmaExamplesRepository()

@vocabulary.route('/revise', methods=['POST'])
@jwt_required
def revise():
    try:
        username = get_jwt_identity()['username']
        minimum_frequency = request.json['minimum_frequency']
        maximum_por = request.json['maximum_por']
        all_learning_lemmas = domain.learning_lemmas_with_probability(username, minimum_frequency,maximum_por)
        payload = JSONEncoder().encode(list(all_learning_lemmas))
        return payload, 200
    except Exception as e:
        current_app.logger.info(str(e))
        return jsonify({'error': str(e)}), 400



@vocabulary.route('/word/<lemma>', methods=['DELETE'])
@jwt_required
def delete(lemma):
    username = get_jwt_identity()['username']
    repository.delete(username, lemma)
    return f'Deleted {lemma}',200

@vocabulary.route('/update_all')
@jwt_required
def update_all():
    domain.request_update_all_examples()
    return 'examples were updated'

