from blinker import Namespace

signals = Namespace()

new_word_to_learn_was_added = signals.signal('new_word_to_learn_was_added')
lemma_examples_were_found = signals.signal('lemma_examples_were_found')

    # word_exposure   = signals.signal('word_exposure')
    # word_review     = signals.signal('word_review')
    #
