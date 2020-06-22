import os

# import spacy

from lib.regex import *


def load_german_prepositions():
    prepositions_file = os.getcwd() + '/config' + '/german_separable_verb_prepositions.txt'

    with open(prepositions_file) as file:
        prepositions = file.read().splitlines()
    return prepositions


class GermanNLPProcessor:

    def __init__(self):
        # self.processor = spacy.load('de_core_news_md')
        self.processor = None
        self.prepositions = load_german_prepositions()


    def make_token_dictionary_and_lemmas_set(self, sentence):

        phrases = breaks_into_phrases_to_detect_separable_verbs.split(sentence)
        token_dictionary = {}
        lemmas_set = set()

        for phrase in phrases:
            tokens = self.processor(phrase)
            if not tokens:
                continue
            separable_verb_tokens, separable_verb_lemma = self.find_possible_separable_verbs(tokens)

            for token in tokens:
                token, lemma = str(token), token.lemma_
                if matches_punctuation.match(token):
                    continue
                if token in separable_verb_tokens:
                    token_dictionary[token] = separable_verb_lemma
                    lemmas_set.add(separable_verb_lemma)
                    continue
                token_dictionary[token] = lemma
                lemmas_set.add(lemma)

        return token_dictionary, lemmas_set

    def find_possible_separable_verbs(self,tokens):
        final_word = tokens[-1].lemma_
        if final_word in self.prepositions:
            for token in tokens:
                if token.tag_[0] == 'V':
                    tokens = [final_word, str(token)]
                    lemma = final_word + token.lemma_
                    return tokens, lemma
        return [], ""
