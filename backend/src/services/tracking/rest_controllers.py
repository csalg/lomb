from operator import itemgetter

from flask_jwt_extended import jwt_required, get_jwt_identity

from flask import Blueprint, request, current_app
from jsonschema import validate

from .domain import Tracker
from .rest_models import *

tracking = Blueprint('tracking', __name__)
tracker = Tracker()


@tracking.route('/', methods=['POST'])
@jwt_required
def rest_handler():
    user = get_jwt_identity()['username']

    content = request.get_json()
    try:
        validate(instance=content, schema=tracking_event_schema)
    except Exception as e:
        current_app.logger.error(str(e))
        return str(e), 422

    message, lemmas, source_language, support_language = itemgetter('message', 'lemmas', 'source_language', 'support_language')(content)
    current_app.logger.info(f"Adding lemma: {content}")
    # tracker.add(user, message, lemmas, source_language, support_language)

    try:
        tracker.add(user, message, lemmas, source_language, support_language)
    except Exception as e:
        current_app.logger.error(str(e))
        return str(e), 500

    return 'ok',200

