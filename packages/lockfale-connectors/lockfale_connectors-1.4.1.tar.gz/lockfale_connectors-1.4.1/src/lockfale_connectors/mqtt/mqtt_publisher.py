import logging
import os

from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from lockfale_connectors.mqtt.mqtt_client import MQTTClientManager

logger = logging.getLogger("console")


class MQTTPublisher(MQTTClientManager):
    """Manages MQTT connections for subscribing and publishing."""

    def __init__(self, client_id: str):
        """Initializes the subscriber client."""
        super().__init__(client_id)

    def publish(self, topic: str, message: str, qos=1):
        """Publishes a message to the MQTT broker."""
        logger.info(f"Publishing to {topic}: {message}")
        publish_properties = Properties(PacketTypes.PUBLISH)
        return self.client.publish(topic, message, qos=qos, properties=publish_properties)
