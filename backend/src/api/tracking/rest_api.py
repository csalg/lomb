import time
from operator import itemgetter

from flask_jwt_extended import jwt_required, get_jwt_identity

from flask import Blueprint, request, current_app, jsonify
from jsonschema import validate

from lib.db import get_db
from mq.signals import StopLearningLemmaEvent
from types_.constants import VALID_MESSAGES
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
    # current_app.logger.info(f"Tracking: {content}")
    # start = int(time.time()*1000)

    controllers.add(user, message, lemmas, source_language, support_language)
    # current_app.logger.info(f'Tracking took {int(time.time()*1000 - start)}')

    return 'ok',200

tracking_event_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string",
                    "enum": VALID_MESSAGES
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
@tracking.route('/delete_word', methods=['POST'])
@jwt_required
def delete():
    try:
        username = get_jwt_identity()['username']
        lemma = request.json['lemma']
        language = request.json['source_language']
        StopLearningLemmaEvent(username, lemma, language).dispatch()
        return f'Deleted {lemma}', 200
    except Exception as e:
        current_app.logger.info(str(e))
        return jsonify({'error': str(e)}), 400
