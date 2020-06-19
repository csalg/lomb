from services.vocabulary.domain import VocabularyDomain


def lemma_examples_were_found_handler(lemma, examples=[]):
    domain = VocabularyDomain()
    domain.update_lemma_examples(lemma, examples)