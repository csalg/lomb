from . import ml

def probability_of_recall_leitner_test():
    sanity_check = [
        (1000, 504325325000, 3),
        (1000, 3, 7495642395432),
        (1000, 3, 10),
        (10000000000, 3, 7495642395432),
    ]

    for args in sanity_check:
        ml.probability_of_recall_leitner(*args)