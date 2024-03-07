from kafka import KafkaProducer
import json
import uuid

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda m: json.dumps(m).encode('utf-8'))


user_id = str(uuid.uuid4())
# Loop to accept user input
while True:
    user_message = input("Enter your message (or type 'exit' to quit): ")
    if user_message.lower() == 'exit':
        break
    message_id = str(uuid.uuid4())  # Generate unique ID for the message
    # producer.send('chat-messages', {'message_id': message_id, 'message': user_message, 'user_id': user_id})
    producer.send('chat-messages', user_message)
    print(f"Sent: {user_message}")

producer.flush()