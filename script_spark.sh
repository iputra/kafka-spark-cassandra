# enter to spark container
docker exec -it spark-master /bin/bash

# submit the app
/opt/spark/bin/spark-submit --master spark://spark-master:7077 \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
    --driver-memory 1G \
    --executor-memory 1G \
    /opt/spark-apps/app_spark.py

# run in the background
nohup /opt/spark/bin/spark-submit --master spark://spark-master:7077 \
    --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 \
    --driver-memory 1G \
    --executor-memory 1G \
    /opt/spark-apps/app_spark.py 2>&1 < /dev/null &

# run with pyspark
./bin/pyspark --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1