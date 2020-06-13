from services.library.domain.domain import LibraryDomain
from mq.signals import lemma_examples_were_found


def new_word_to_learn_was_added_handler(lemma):
    # print(f'{lemma} was added')
    domain = LibraryDomain(nlp_processor=lambda:0)
    examples = domain.find_examples(lemma)
    # print('examples were found!')
    lemma_examples_were_found.send(lemma, examples=examples)
    # print(list(examples))
    ## Needs to find


# def new_book_was_added(book_id):
#     domain = LibraryDomain(nlp_processor=lambda:0)
#     examples = domain.find_examples_in_book(book_id)
#     lemma_examples_were_found.send(lemma, examples=examples)
