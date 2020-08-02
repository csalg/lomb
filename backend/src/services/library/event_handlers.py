from flask import current_app

from mq.signals import lemma_examples_were_found


def new_lemma_was_added_handler(payload):
    # current_app.logger.info(payload)
    # try:
    #     examples = list(Library.get_examples(payload[ "lemma" ],  payload['source_language'], payload['support_language'],textfiles=None))
    #     lemma_examples_were_found.send({'context': payload, 'examples':examples})
    #     return examples
    # except Exception as e:
    #     current_app.logger.error(e)
    pass
