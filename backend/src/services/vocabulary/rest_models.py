from config import MINIMUM_LEARNING_LEMMA_FREQUENCY_ALLOWED_FOR_REVISION

learning_lemmas_request = {
    "type": "object",
    "properties": {
        "minimum_frequency": {"type": "integer",
                              "minimum": MINIMUM_LEARNING_LEMMA_FREQUENCY_ALLOWED_FOR_REVISION },
    },
    "required": ["minimum_frequency"]
}