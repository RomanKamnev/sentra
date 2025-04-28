import json
from kafka import KafkaConsumer

def main():
    # Создаём Kafka consumer
    consumer = KafkaConsumer(
        'logs-events',  # <-- правильное название топика
        bootstrap_servers=['localhost:9092'],  # адрес брокера Kafka
        auto_offset_reset='earliest',          # читаем сначала
        enable_auto_commit=True,               # автокоммит оффсета
        group_id='log-consumer-group',          # ID группы консюмеров
        value_deserializer=lambda x: x.decode('utf-8')  # декодируем байты в строку
    )

    print("Listening for logs...")
    try:
        for message in consumer:
            try:
                log = message.value
                print(f"Received LOG: {log}")
            except json.JSONDecodeError:
                print(f"Received non-JSON message: {message.value}")
    except KeyboardInterrupt:
        print("\nStopped by user")

if __name__ == '__main__':
    main()
