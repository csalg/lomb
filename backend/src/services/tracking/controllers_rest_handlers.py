import json
from operator import itemgetter

from flask_jwt_extended import jwt_required, get_jwt_identity

from flask import Blueprint, request, current_app
from jsonschema import validate

from lib.db import get_db
from .controllers import create_controllers_with_mongo_repositories
from .controllers_rest_models  import *


tracking = Blueprint('tracking', __name__)
db = get_db()
controllers = create_controllers_with_mongo_repositories(db)


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
    current_app.logger.info(f"Tracking: {content}")
    # tracker.add(user, message, lemmas, source_language, support_language)

    try:
        controllers.add(user, message, lemmas, source_language, support_language)
    except Exception as e:
        current_app.logger.error(str(e))
        return str(e), 400

    return 'ok',200

