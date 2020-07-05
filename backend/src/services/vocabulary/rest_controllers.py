
from flask import Blueprint, render_template
from flask.json import JSONEncoder
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.vocabulary.infrastructure.signals import lemma_examples_were_found_handler
from .domain import VocabularyDomain
from mq.signals import lemma_examples_were_found

vocabulary = Blueprint('vocabulary', __name__, template_folder='templates')
domain = VocabularyDomain()
lemma_examples_were_found.connect(lemma_examples_were_found_handler)


@vocabulary.route('/revise')
@jwt_required
def revise():
    username = get_jwt_identity()['username']
    all_learning_lemmas = domain.learning_lemmas(username)
    payload = JSONEncoder().encode(list(all_learning_lemmas))
    return payload, 200


@vocabulary.route('/update_all')
@jwt_required
def update_all():
    domain.request_update_all_examples()
    return 'examples were updated'

