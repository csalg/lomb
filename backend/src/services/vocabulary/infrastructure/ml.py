limit = lambda n, minn, maxn: max(min(maxn, n), minn)

def probability_of_recall_leitner(elapsed, successes, failures):
    delta = elapsed/(60*60)
    success_failure_difference = limit(successes - failures, -20, 20)
    try:
        h = 2.0 ** success_failure_difference
        p = 2.0 ** (-(delta / h))
    except Exception as e:
        raise Exception(f'Got {str(e)} with {elapsed, successes, failures}')
    return p
