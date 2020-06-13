

def probability_of_recall_leitner(elapsed, previous_elapsed, successes, failures):
    if elapsed == 0 or previous_elapsed == 0:
        return 0
    delta = elapsed/previous_elapsed
    h = successes - failures
    h = max(h, 1)
    p = 2.0 ** (-(delta / h))
    return p
