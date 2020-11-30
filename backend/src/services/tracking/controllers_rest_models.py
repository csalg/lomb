from services.tracking.message_constants import valid_messages

tracking_event_schema = {
    "type": "object",
    "properties": {
        "message": {"type": "string",
                    "enum": valid_messages
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
