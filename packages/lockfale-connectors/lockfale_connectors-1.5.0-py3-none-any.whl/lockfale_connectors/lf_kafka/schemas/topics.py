from lockfale_connectors.lf_kafka.schemas.base import BASE_FIELDS, BASE_FIELDS_REQUIRED
from lockfale_connectors.lf_kafka.schemas.cyberpartner import CP

TOPIC_SCHEMAS = {
    "producers": {
        "cyberpartner-event-log": {
            "type": "object",
            "properties": {"message_received_ts": {"type": "string"}, **BASE_FIELDS},
            "required": [
                "message_received_ts"
            ] + BASE_FIELDS_REQUIRED,
        },
        "ingress-cackalacky-cyberpartner-create": {
            "type": "object",
            "properties": {"badge_id": {"type": "string"}, "requester": {"type": "string"}, "cp_obj": CP, **BASE_FIELDS},
            "required": ["badge_id"] + BASE_FIELDS_REQUIRED,
        },
        "ingress-cackalacky-cyberpartner-state-update": {
            "type": "object",
            "properties": {"badge_id": {"type": "string"}, "cp_obj": CP, **BASE_FIELDS},
            "required": ["badge_id", "cp_obj"] + BASE_FIELDS_REQUIRED,
        },
    }
}
