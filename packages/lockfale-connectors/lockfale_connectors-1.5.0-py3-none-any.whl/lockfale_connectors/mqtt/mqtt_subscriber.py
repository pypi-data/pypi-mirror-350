import logging
import os

from lockfale_connectors.mqtt.mqtt_client import MQTTClientManager
from lockfale_connectors.mqtt.mqtt_handlers import (
    on_connect,
    on_message,
    on_subscribe,
    on_unsubscribe,
)

logger = logging.getLogger("console")


class MQTTSubscriber(MQTTClientManager):
    """Manages MQTT connections for subscribing to MQTT topics."""

    def __init__(self, client_id: str, _on_connect=on_connect, _on_message=on_message, _on_subscribe=on_subscribe, _on_unsubscribe=on_unsubscribe):
        """Initializes the subscriber client."""
        super().__init__(client_id)  # Calls the constructor of MQTTClientManager

        self.custom_callbacks = {
            "on_connect": _on_connect,
            "on_message": _on_message,
            "on_subscribe": _on_subscribe,
            "on_unsubscribe": _on_unsubscribe,
        }

        # Now configure event handlers for subscription
        self.configure_subscriber()

    def configure_subscriber(self):
        """Attaches event handlers for subscriber client."""
        self.client.on_connect = self.custom_callbacks["on_connect"]
        self.client.on_message = self.custom_callbacks["on_message"]
        self.client.on_subscribe = self.custom_callbacks["on_subscribe"]
        self.client.on_unsubscribe = self.custom_callbacks["on_unsubscribe"]

    def start_listener(self):
        """Starts the subscriber in a non-blocking way."""
        logger.info("Starting MQTT listener...")
        self.client.loop_start()
