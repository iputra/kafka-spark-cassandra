# enter the container 
docker exec -it cassandra1 bash -c 'cqlsh'

# create user keyspace / database
CREATE KEYSPACE IF NOT EXISTS db_chat WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

# create table
USE db_chat;

CREATE TABLE IF NOT EXISTS tbl_messages (
    message_id uuid PRIMARY KEY,
    message text,
);

# verify 
DESCRIBE tbl_messages;
SELECT * FROM tbl_messages;

# delete table
DROP TABLE db_chat.tbl_messages;

# delete all data
TRUNCATE tbl_messages;