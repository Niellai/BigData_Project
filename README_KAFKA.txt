# To start kafka zookeeper and server
1. Change to dir
   cd /usr/local/kafka

2. Start Kafka Zookeeper, open new terminal
bin/zookeeper-server-start.sh config/zookeeper.properties

3. Start Kafka Server, open new terminal
bin/kafka-server-start.sh config/server.properties




# Consumer kafka
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic testTopic --from-beginning
