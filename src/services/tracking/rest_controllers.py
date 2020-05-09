from operator import itemgetter

from flask import Blueprint, request
from jsonschema import validate

from config import DEBUG

from .rest_models import *
from .db_repository import TrackingRepository


tracking = Blueprint('tracking', __name__)
event_types = ['EXPOSURE', 'REVIEW']
repository = TrackingRepository()


@tracking.route('/', methods=['POST'])
def rest_handler():
    content = request.get_json()
    try:
        validate(instance=content, schema=tracking_event_schema)
    except Exception as e:
        return str(e) if DEBUG else ""
    
    type_, payload, context = itemgetter('type', 'payload', 'context')(content)

    if type_ == 'SENTENCE_EXPOSURE':
        repository.add_phrase_exposure(context, payload == 'LOOKUP')
    elif type_ == 'WORD_EXPOSURE':
        repository.add_direct_word_lookup(context)
    elif type_ == 'REVIEW':
        repository.add_review(context, payload == "CLICK")
    else:
        return 'wrong type'

    return 'ok'


