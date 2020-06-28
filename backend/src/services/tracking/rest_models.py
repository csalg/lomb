
tracking_event_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string",
                    "enum": [
                            "TEXT__WORD_HIGHLIGHTED",
                            "TEXT__SENTENCE_CLICK",
                            "TEXT__SENTENCE_READ"
                            ]
                    },
        "lemmas": {"type": "array",
                     "items": {
                         "type": "string"
                        }
                     }
    }
}