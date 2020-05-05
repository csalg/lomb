from operator import itemgetter

from flask import Blueprint, request
from jsonschema import validate

from config import DEBUG
from mq.signals import exposure_was_received

from .rest_models import *
from . import domain

tracking = Blueprint('tracking', __name__)

event_types = ['EXPOSURE', 'REVIEW']

@tracking.route('/', methods=['POST'])
def rest_handler():
    content = request.get_json()
    try:
        validate(instance=content, schema=tracking_event_schema)
    except Exception as e:
        if DEBUG:
            return str(e) if DEBUG else ""
    
    type_, payload, context = itemgetter('type', 'payload', 'context')(content)

    if type_ == 'EXPOSURE':
        exposure_was_received.send(payload,context=context)
    if type_ == 'REVIEW':
        pass

    return 'ok'
