from kafka import KafkaConsumer
from config import KAFKA_BROKER, ALERTS_TOPIC, GROUP_ID

def create_consumer():
    consumer = KafkaConsumer(
        ALERTS_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id=GROUP_ID,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda v: v.decode('utf-8')
    )
    return consumer
