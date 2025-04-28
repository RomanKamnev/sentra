from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'alerts',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='alert-monitor-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

print("🟢 Listening for alerts on topic 'alerts'...")

try:
    for message in consumer:
        print(f"🚨 ALERT RECEIVED: {message.value}")
except KeyboardInterrupt:
    print("🛑 Stopped listening.")
