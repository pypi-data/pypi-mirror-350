import json
import logging
from typing import List

from kafka import KafkaConsumer as KConsumer

logger = logging.getLogger("console")


class KafkaConsumer:
    """ensuring build"""
    def __init__(self, kafka_broker: str, topics: List[str], group_id: str):
        self.kafka_broker = kafka_broker
        self.topics = topics
        self.group_id = group_id
        self.consumer = self._create_consumer()

    def _create_consumer(self):
        """Initialize and return a Kafka producer"""
        return KConsumer(
            *self.topics,
            bootstrap_servers=self.kafka_broker,
            auto_offset_reset="latest",
            enable_auto_commit=True,
            group_id=self.group_id,
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )

    def disconnect(self):
        """Flush and close the Kafka consumer"""
        if self.consumer:
            self.consumer.close()
            logger.info("Kafka consumer disconnected.")
