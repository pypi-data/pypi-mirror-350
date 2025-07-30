import json
import logging
from datetime import datetime, timezone
from typing import Dict, Optional

from jsonschema import ValidationError, validate
from kafka import KafkaProducer as KProducer

from lockfale_connectors.lf_kafka.schemas.topics import TOPIC_SCHEMAS

logger = logging.getLogger("console")

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


def enrich_message_timestamp(message: Dict) -> Dict:
    now_utc = datetime.now(timezone.utc)
    if not message.get("ts"):
        # badge didn't send a timestamp, so we create one
        epoch_ts = now_utc.timestamp()
        message["ts"] = epoch_ts

    if message.get("ts") and not message.get("event_timestamp"):
        # that means this is from a badge and not yet enriched
        # expected type is epoch
        dt = datetime.fromtimestamp(message.get("ts"), tz=timezone.utc)
        formatted_ts = dt.strftime(TIMESTAMP_FORMAT)[:-3]
        message["event_timestamp"] = formatted_ts

    if not message.get("event_timestamp"):
        # internal, not enriched, no idea why not, but here's the failsafe
        ts_utc = now_utc.strftime(TIMESTAMP_FORMAT)[:-3]
        message["event_timestamp"] = ts_utc

    return message


def enrich_message(source_topic: str, message: Optional[Dict] = None) -> Optional[Dict]:
    if not message:
        message = {}

    badge_id = message.get("badge_id")
    if "/" in source_topic:
        # From MQTT => extract badge_id from source topic
        topic_parts = source_topic.split("/")
        badge_id = topic_parts[3] if len(topic_parts) > 3 else None

    if not badge_id:
        logger.error(f"Cannot find badge_id... returning None")
        return None

    message = enrich_message_timestamp(message)
    message['badge_id'] = badge_id
    return message


def validate_message(destination_topic: str, message: Dict):
    schema = TOPIC_SCHEMAS.get("producers").get(destination_topic)
    if schema:
        validate(instance=message, schema=schema)


class KafkaProducer:
    def __init__(self, kafka_broker: str):
        self.kafka_broker = kafka_broker
        self.producer = self._create_producer()

    def _create_producer(self):
        """Initialize and return a Kafka producer"""
        return KProducer(
            bootstrap_servers=self.kafka_broker,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
            acks="all",
            retries=3,
            connections_max_idle_ms=10 * 60 * 1000 # 10min
        )

    def disconnect(self):
        """Flush and close the Kafka producer"""
        if self.producer:
            try:
                self.producer.flush()
                self.producer.close()
                logger.info("Kafka producer disconnected.")
            except Exception as e:
                logger.warning(f"Exception while closing producer: {e}")

    def _reconnect(self):
        """Reconnects by creating a new Kafka producer"""
        logger.warning("Reconnecting Kafka producer...")
        self.disconnect()
        self.producer = self._create_producer()

    def send_message(self, source_topic: str, destination_topic: str, message: Dict, key: str = None):
        """Send a message to Kafka."""
        try:
            if not self.producer:
                logger.warning("Kafka producer invalid, reconnecting...")
                self._reconnect()

            if self.producer._closed:
                logger.warning("Kafka producer closed, reconnecting...")
                self._reconnect()

            _key = None
            if isinstance(key, str):
                _key = key.encode("utf-8")

            message = enrich_message(source_topic=source_topic, message=message)
            validate_message(destination_topic=destination_topic, message=message)
            future = self.producer.send(destination_topic, key=_key, value=message)
            record_metadata = future.get(timeout=10)
            logger.info(f"Message sent to {record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}")
            logger.info(f"Message content: {json.dumps(message)}")
            return True
        except Exception as e:
            logger.exception(f"Failed to send message: {e}")
            return False
