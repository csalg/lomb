
def calculate_probabilities(username, language, lemmas=None):
    # Maybe lemmas can be an array of dictionaries? This
    # would allow to keep data like frequency together.
    #
    # Grab datapoints from db
    # Put everything into a df, including score data
    # Calculate all the scores
    # Calculate all the PoR
    # Create an additional column with the result, by masking out
    # PoR if scores should take precedence`
    # Remove all the additional data and return the result and the
    # index (the lemmas) as an array of tuples.
    if lemmas is None:
        # Calculate all probabilities
        pass
    pass
