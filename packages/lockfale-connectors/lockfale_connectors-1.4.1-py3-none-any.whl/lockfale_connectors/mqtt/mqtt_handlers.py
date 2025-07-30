import logging

logger = logging.getLogger("console")

# Static topic routes
TOPIC_ROUTE_MAPPING = {
    "default": lambda topic, payload: logger.info(f"Message: {payload.decode('utf-8')}"),
}


def matching_topic_handler(topic):
    """Finds a matching function for the given topic"""
    if topic in TOPIC_ROUTE_MAPPING:
        return TOPIC_ROUTE_MAPPING[topic]

    return TOPIC_ROUTE_MAPPING["default"]


def on_connect(client, userdata, flags, reason_code, properties):
    """Handles MQTT connection"""
    logger.info(f"Connected with result code: {reason_code}")

    if reason_code.is_failure:
        logger.error(f"Failed to connect: {reason_code}")
        return

    subscription_list = [
        ("cackalacky/badge/egress/+/cyberpartner/create", 1),
    ]
    client.subscribe(subscription_list)


def on_message(client, userdata, message):
    """Handles incoming MQTT messages"""
    if message.retain:
        logger.info("Skipping retained message")
        return

    logger.info(message.topic)
    logger.info(message.payload)
    handler = matching_topic_handler(message.topic)
    handler(message.topic, message.payload)


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    """Handles MQTT subscription acknowledgment"""
    for reason_code in reason_code_list:
        if reason_code.is_failure:
            logger.error(f"Subscription rejected: {reason_code}")
        else:
            logger.info(f"Subscribed with QoS: {reason_code.value}")


def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    """Handles MQTT unsubscription acknowledgment"""
    if not reason_code_list or not reason_code_list[0].is_failure:
        logger.info("Unsubscribe succeeded")
    else:
        logger.error(f"Unsubscribe failed: {reason_code_list[0]}")
