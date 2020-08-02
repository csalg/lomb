tracking_event_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string",
                    "enum": [
                        "TEXT__WORD_HIGHLIGHTED",
                        "TEXT__SENTENCE_CLICK",
                        "TEXT__SENTENCE_READ",
                        "REVISION__CLICKED",
                        "REVISION__NOT_CLICKED"
                    ]
                    },
        "lemmas": {"type": "array",
                   "items": {
                       "type": "string"
                   }
                   },
        "source_language": {'type': 'string'},
        "support_language": {'type': 'string'}
    },
    "required": ["message", "lemmas", "source_language"]
}
