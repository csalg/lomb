
tracking_event_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "payload": {"type": "string"}, 
        "examples": {"type": "string"},
        "context": {"type": "array",
                     "items": {
                         "type": "string"
                     }
                     }
    }
}