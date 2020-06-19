from flask import Blueprint, render_template

from services.vocabulary.infrastructure.signals import lemma_examples_were_found_handler
from .domain import VocabularyDomain
from mq.signals import lemma_examples_were_found

vocabulary = Blueprint('vocabulary', __name__, template_folder='templates')
domain = VocabularyDomain()
lemma_examples_were_found.connect(lemma_examples_were_found_handler)


@vocabulary.route('/learning')
def learning():

    all_learning_lemmas = domain.learning_lemmas_with_probability()
    return render_template('lemmas_learning.html.j2',
                           lemmas=all_learning_lemmas)

@vocabulary.route('/update_all')
def update_all():
    domain.request_update_all_examples()
    return 'examples were updated'

# @vocabulary.route('/book/<id>')
# def book(id):
#     book = repository.get_book(id)
#     # print(len(book['chunks']))
#     if book:
#         return render_template('text.html.j2', **book)
#     return f'Id {id} not found!'
