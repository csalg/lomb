from operator import itemgetter

from flask_jwt_extended import jwt_required, get_jwt_identity

from flask import Blueprint, request, current_app
from jsonschema import validate

from lib.db import get_db
from mq.signals import StopLearningLemmaEvent
from .constants import valid_messages
from .controllers import create_controllers_with_mongo_repositories

tracking = Blueprint('tracking', __name__)
db = get_db()
controllers = create_controllers_with_mongo_repositories(db)

def stop_learning_lemma_handler(stop_learning_lemma_event):
    current_app.logger.info('Inside tracking')
    controllers.ignore_lemma(stop_learning_lemma_event.username, stop_learning_lemma_event.lemma, stop_learning_lemma_event.source_language)
StopLearningLemmaEvent.addEventListener(stop_learning_lemma_handler)


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

    controllers.add(user, message, lemmas, source_language, support_language)

    return 'ok',200

tracking_event_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string",
                    "enum": valid_messages
                    },
        "lemmas": {"type": "array",
                   "items": {
                       "type": "string"
                   }
                   },
        "source_language": {'type': 'string'},
        "support_language": {'type': 'string'}
    },
    "required": ["message", "lemmas", "source_language"]
}
