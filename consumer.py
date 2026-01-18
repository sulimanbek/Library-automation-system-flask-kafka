from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'your_topic',
    bootstrap_servers='localhost:5001',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    print(message.value)
