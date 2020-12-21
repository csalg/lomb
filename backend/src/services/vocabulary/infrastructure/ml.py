

def probability_of_recall_leitner(elapsed, successes, failures):
    if elapsed == 0 or previous_elapsed == 0:
        return 0
    delta_hours = elapsed/(60*60)
    h = 2.0 ** (successes - failures)
    p = 2.0 ** (-(delta / h))
    return p
