from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr
import uuid
import json

def init_spark():
  spark = SparkSession.builder \
    .appName("chat-messages-app") \
    .config("spark.cassandra.connection.host", "cassandra1") \
    .config("spark.cassandra.connection.port", 9042) \
    .getOrCreate()
  sc = spark.sparkContext
  return spark, sc

spark, sc = init_spark()

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "kafka1:19092") \
  .option("subscribe", "chat-messages") \
  .load() \
  .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

help_messages = df.filter("value LIKE '%help%'")
other_messages = df.filter("value NOT LIKE '%help%'")

kafka_sink = help_messages \
    .writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka1:19092") \
    .option("topic", "help-messages") \
    .option("checkpointLocation", "/tmp/kafka/checkpoint") \
    .start()

other_messages_transformed = other_messages \
    .withColumn("message_id", expr("uuid()")) \
    .select(
        col("message_id"),
        col("value").alias("message")  # Rename 'value' column to 'message'
    )

cassandra_sink = other_messages_transformed \
    .writeStream \
    .foreachBatch(lambda batch_df, _: batch_df.write \
                  .format("org.apache.spark.sql.cassandra") \
                  .option("keyspace", "db_chat") \
                  .option("table", "tbl_messages") \
                  .mode("append") \
                  .save()) \
    .option("checkpointLocation", "/tmp/cassandra/checkpoint") \
    .start()

kafka_sink.awaitTermination()
cassandra_sink.awaitTermination()
