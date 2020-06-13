from operator import itemgetter

from config import DEBUG
from flask import Blueprint, request
from jsonschema import validate

from .domain import TrackingDomain
from .rest_models import *

tracking = Blueprint('tracking', __name__)
event_types = ['EXPOSURE', 'REVIEW']
domain = TrackingDomain()


@tracking.route('/', methods=['POST'])
def rest_handler():
    content = request.get_json()
    print(content)

    # try:
    #     validate(instance=content, schema=tracking_event_schema)
    # except Exception as e:
    #     return str(e) if DEBUG else ""
    validate(instance=content, schema=tracking_event_schema)

    type_, payload, context = itemgetter('type', 'payload', 'context')(content)

    print(type_, payload, context)

    if type_ == 'SENTENCE_EXPOSURE':
        lemmas, was_looked_up = context, payload == 'LOOKUP'
        domain.add_sentence_exposure(lemmas, was_looked_up)
    elif type_ == 'WORD_EXPOSURE':
        domain.add_direct_word_lookup(context)
    elif type_ == 'REVIEW':
        word, was_clicked = context[0], payload == 'CLICK'
        examples = int(content['examples'])
        domain.add_review(word, was_clicked, examples)
    else:
        return 'wrong type'

    return 'ok'

