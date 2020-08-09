from flask import current_app

from mq.signals import LemmaExamplesWereFoundEvent
from services.vocabulary.domain import VocabularyDomain


def lemma_examples_were_found_handler(lemma_examples: LemmaExamplesWereFoundEvent):
    examples = [ {'text': example['text'],
                  'support_text': example['support_text'],
                  'source_language': example['source_language'],
                  'support_language': example['support_language'],
                  } for example in lemma_examples.examples]
    domain = VocabularyDomain()
    domain.update_lemma_examples(lemma_examples.user,lemma_examples.lemma,lemma_examples.source_language,examples)