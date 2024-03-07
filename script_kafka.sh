# enter to kafka container
docker exec -it kafka1 /bin/bash

# create kafka topic
kafka-topics --version
kafka-topics --bootstrap-server localhost:9092 --topic chat-messages --create --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --topic help-messages --create --partitions 1 --replication-factor 1

# verify kafka topic
kafka-topics --bootstrap-server localhost:9092 --list

# delete kafka topic
kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic chat-messages

# listen message on topic
kafka-console-consumer --bootstrap-server localhost:9092 --topic chat-messages

# listen message on topic from beginning
kafka-console-consumer --bootstrap-server localhost:9092 --topic help-messages --from-beginning