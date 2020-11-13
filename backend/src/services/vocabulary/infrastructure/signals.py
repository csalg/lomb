import logging

from mq.signals import LemmaExamplesWereFoundEvent
from services.vocabulary.controllers import Controllers

domain = Controllers()


def lemma_examples_were_found_handler(lemma_examples: LemmaExamplesWereFoundEvent):
    examples = [ {'text': example['text'],
                  'support_text': example['support_text'],
                  'source_language': example['source_language'],
                  'support_language': example['support_language'],
                  } for example in lemma_examples.examples]

    logging.info('Received LemmaExamplesWereFoundEvent')
    domain.update_lemma_examples(lemma_examples.user,lemma_examples.lemma,lemma_examples.source_language,examples, lemma_examples.frequency)