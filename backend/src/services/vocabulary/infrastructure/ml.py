

def probability_of_recall_leitner(elapsed, successes, failures):
    delta = elapsed/(60*60)
    h = 2.0 ** (successes - failures)
    p = 2.0 ** (-(delta / h))
    return p
