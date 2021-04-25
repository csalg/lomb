from flask import Blueprint, request, current_app
from flask.json import JSONEncoder, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt

from config import MINIMUM_LEARNING_LEMMA_FREQUENCY_ALLOWED_FOR_REVISION
from mq.signals import LemmaExamplesWereFoundEvent, StopLearningLemmaEvent
from services.vocabulary.infrastructure.signals import lemma_examples_were_found_handler
from .db import LemmaExamplesRepository
from .controllers import Controllers, ReviseQueryDTO

vocabulary = Blueprint('vocabulary', __name__, template_folder='templates')
domain = Controllers()
LemmaExamplesWereFoundEvent.addEventListener(lemma_examples_were_found_handler)
repository = LemmaExamplesRepository()


@vocabulary.route('/revise', methods=['POST'])
@jwt_required
def revise():
    try:
        dto = ReviseQueryDTO(
            get_jwt_identity()['username'],
            request.json['minimum_frequency'],
            float(request.json['maximum_por']),
            request.json['maximum_days_elapsed'],
            request.json['use_smart_fetch']
        )
        all_learning_lemmas = domain.learning_lemmas_with_probability(dto)
        payload = JSONEncoder().encode(list(all_learning_lemmas))
        return payload, 200
    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({'error': str(e)}), 400


@vocabulary.route('/delete_word', methods=['POST'])
@jwt_required
def delete():
    try:
        username = get_jwt_identity()['username']
        lemma = request.json['lemma']
        language = request.json['source_language']
        repository.delete(username, lemma, language)
        StopLearningLemmaEvent(username, lemma, language).dispatch()
        return f'Deleted {lemma}', 200
    except Exception as e:
        current_app.logger.info(str(e))
        return jsonify({'error': str(e)}), 400


@vocabulary.route('/heatmap/<resolution>/<neighbours>')
def heatmap(resolution, neighbours):
    username = 'charlie'
    fig = domain.heatmap(username, int(resolution), int(neighbours))
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


learning_lemmas_request = {
    "type": "object",
    "properties": {
        "minimum_frequency": {"type": "integer",
                              "minimum": MINIMUM_LEARNING_LEMMA_FREQUENCY_ALLOWED_FOR_REVISION},
        "maximum_por": {"type": "number",
                        "minimum": 0,
                        "maximum": 1
                        },
    },
    "required": ["minimum_frequency", "maximum_por"]
}
