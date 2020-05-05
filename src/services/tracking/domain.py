from mq.signals import exposure_was_received, word_exposure
from common.regex import matches_punctuation

@exposure_was_received.connect
def exposure_was_received_handler(payload, context=""):
    if context:
        was_looked_up = payload == 'LOOKUP'
        words = matches_punctuation.split(context)
        for word in words:
            if word:
                word_exposure.send(word, was_looked_up=was_looked_up)