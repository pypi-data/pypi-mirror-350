CP = {
    "type": "object",
    "properties": {
        "cp": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "family": {"type": "string"},
                "archetype": {"type": "string"},
                "sprite": {"type": "string"},
                "stats": {
                    "type": "object",
                    "properties": {
                        "strength": {"type": "integer"},
                        "defense": {"type": "integer"},
                        "evade": {"type": "integer"},
                        "accuracy": {"type": "integer"},
                        "speed": {"type": "integer"},
                        "vision": {"type": "integer"},
                    },
                    "required": ["strength", "defense", "evade", "accuracy", "speed", "vision"],
                },
                "stat_modifiers": {
                    "type": "object",
                    "properties": {
                        "age": {"type": "object", "properties": {"multiplier": {"type": "number"}}, "required": ["multiplier"]},
                        "hunger": {"type": "object", "properties": {"multiplier": {"type": "number"}}, "required": ["multiplier"]},
                        "thirst": {"type": "object", "properties": {"multiplier": {"type": "number"}}, "required": ["multiplier"]},
                        "weight": {"type": "object", "properties": {"multiplier": {"type": "number"}}, "required": ["multiplier"]},
                        "happiness": {"type": "object", "properties": {"multiplier": {"type": "number"}}, "required": ["multiplier"]},
                    },
                    "required": ["age", "hunger", "thirst", "weight", "happiness"],
                },
                "user_id": {"type": "integer"},
                "is_active": {"type": "integer"},
                "id": {"type": "integer"},
            },
            "required": ["name", "family", "archetype", "stat_modifiers"],
        },
        "state": {
            "type": "object",
            "properties": {
                "status": {"type": "integer"},
                "life_phase": {"type": "string"},
                "life_phase_change_timestamp": {"type": "string"},
                "wellness": {"type": "integer"},
                "disposition": {"type": "integer"},
                "age": {"type": "integer"},
                "hunger": {"type": "integer"},
                "thirst": {"type": "integer"},
                "weight": {"type": "integer"},
                "happiness": {"type": "integer"},
                "health": {"type": "integer"},
            },
            "required": ["status", "wellness", "disposition", "age", "hunger", "thirst", "weight", "happiness", "health"],
        },
        "attributes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "group": {"type": "string"},
                    "name": {"type": "string"},
                    "multiplier": {"type": "number"},
                    "chance": {"type": "number"},
                },
                "required": ["group", "name", "multiplier", "chance"],
            },
        },
    },
    "required": ["cp", "state", "attributes"],
}
