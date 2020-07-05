from flask import current_app

from services.vocabulary.domain import VocabularyDomain


def lemma_examples_were_found_handler(payload):
    current_app.logger.info('In Vocabulary we received:')
    current_app.logger.info(payload)
    user, lemma = payload['context']['user'], payload['context']['lemma']
    examples = [ {'text': example['text'], 'support_text': example['support_text']} for example in payload['examples']]
    current_app.logger.info(f"Will add: user: {user}, lemma: {lemma}, examples: {examples}")
    domain = VocabularyDomain()
    domain.update_lemma_examples(user,lemma, examples)