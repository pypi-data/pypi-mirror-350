BASE_FIELDS = {
    "event_source": {"type": "string"},
    "event_subtype": {"type": "string"},
    "event_timestamp": {"type": "string"},
    "event_type": {"type": "string"},
    "event_uuid": {"type": "string"},
}

BASE_FIELDS_REQUIRED = ["event_source", "event_subtype", "event_timestamp", "event_type", "event_uuid"]
