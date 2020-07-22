from config import MINIMUM_LEARNING_LEMMA_FREQUENCY_ALLOWED_FOR_REVISION

learning_lemmas_request = {
    "type": "object",
    "properties": {
        "minimum_frequency": {"type": "integer",
                              "minimum": MINIMUM_LEARNING_LEMMA_FREQUENCY_ALLOWED_FOR_REVISION},
        "maximum_por": {"type": "number",
                        "minimum": 0,
                        "maximum": 1
                        },
    },
    "required": ["minimum_frequency", "maximum_por"]
}
