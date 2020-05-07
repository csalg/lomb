from operator import itemgetter

from flask import Blueprint, request
from jsonschema import validate

from config import DEBUG

from .rest_models import *
from .domain import exposure_was_received_handler, review_was_received_handler


tracking = Blueprint('tracking', __name__)
event_types = ['EXPOSURE', 'REVIEW']


@tracking.route('/', methods=['POST'])
def rest_handler():
    content = request.get_json()
    try:
        validate(instance=content, schema=tracking_event_schema)
    except Exception as e:
        return str(e) if DEBUG else ""
    
    type_, payload, context = itemgetter('type', 'payload', 'context')(content)

    if type_ == 'EXPOSURE':
        exposure_was_received_handler(context, payload == 'LOOKUP')
    elif type_ == 'REVIEW':
        review_was_received_handler(context, payload == "CLICK")
    else:
        return 'wrong type'

    return 'ok'


