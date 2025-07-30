import logging
import os
import ssl

import paho.mqtt.client as mqtt

logger = logging.getLogger("console")


class MQTTClientManager:
    """Manages MQTT connections for subscribing and publishing."""

    def __init__(self, client_id: str):
        """Initializes both subscriber and publisher clients."""
        self.mqtt_host = os.getenv("MQTT_HOST")
        self.mqtt_port = int(os.getenv("MQTT_PORT", 1883))
        self.client_id = f"{client_id}-{os.getenv('DOPPLER_ENVIRONMENT')}"

        self._create_mqtt_client()

    def _create_mqtt_client(self):
        """Creates and configures an MQTT client."""
        logger.info(f"Creating client: {self.client_id}")
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=self.client_id, protocol=mqtt.MQTTv311, transport="tcp"
        )

        self.client.username_pw_set(username=os.getenv("MQTT_USERNAME"), password=os.getenv("MQTT_PASSWORD"))

    def set_tls(self):
        """Attaches TLS to the client."""
        if os.getenv("MQTT_USE_TLS", "false").lower() == "true":
            self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)

    def connect(self, keep_alive: int = 60):
        """Connect the client to the broker."""
        logger.info(f"Connecting to {self.mqtt_host}:{self.mqtt_port}...")
        self.client.connect(self.mqtt_host, self.mqtt_port, keepalive=keep_alive)

    def disconnect(self):
        """Disconnect the client to the broker."""
        logger.info(f"Disconnecting from {self.mqtt_host}:{self.mqtt_port}...")
        self.client.disconnect()
