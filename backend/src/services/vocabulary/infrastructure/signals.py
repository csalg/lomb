from flask import current_app

from services.vocabulary.domain import VocabularyDomain


def lemma_examples_were_found_handler(payload):
    current_app.logger.info('In Vocabulary we received:')
    current_app.logger.info(payload)
    user, lemma, language = payload['context']['user'], payload['context']['lemma'], payload['context']['source_language']
    examples = [ {'text': example['text'],
                  'support_text': example['support_text'],
                  'source_language': example['source_language'],
                  'support_language': example['support_language'],
                  } for example in payload['examples']]
    current_app.logger.info(f"Will add: user: {user}, lemma: {lemma}, examples: {examples}")
    domain = VocabularyDomain()
    domain.update_lemma_examples(user,lemma, language,examples)