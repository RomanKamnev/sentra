import json
import random
import time
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

event_types = ['ssh', 'ftp', 'web_login_failed', 'credential_stuffing']

usernames = [
    'admin', 'user', 'test', 'guest', 'root', 'operator', 'manager',
    'login', 'support', 'dev', 'qa', 'john', 'jane', 'alice', 'bob'
]

ips = [
    '192.168.0.1',
]

print("🟢 Starting log generation...")

for _ in range(100):
    event_type = random.choice(event_types)
    ip = random.choice(ips)
    username = random.choice(usernames)
    failures = random.randint(5, 10) if event_type != 'credential_stuffing' else 1

    log = {
        "event_type": event_type,
        "ip": ip,
        "username": username,
        "failures": failures,
        "timestamp": time.time()
    }

    producer.send("logs", log)
    print(f"Sent: {log}")

    time.sleep(random.uniform(0.2, 0.8))

print("🛑 Finished log generation.")
