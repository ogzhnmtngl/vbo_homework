# QUESTIONS
Set up a 3-node kafka cluster as you see in the class using docker-compose.
## 1.
Create a topic named `atscale`, 2 partitions and replication factor 1.

/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 \
--create --topic atscale \
--replication-factor 1 \
--partitions 2

## 2. 
List all topics.
```
root@0e1e0b5ab6af:/# /kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
__consumer_offsets
_schemas
atscale
```

## 3. 
Describe `atscale` topic.
```
root@0e1e0b5ab6af:/# /kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 \
> --describe --topic atscale
Topic: atscale  TopicId: FqwnOraRSyCwGynGAN9PzA PartitionCount: 2       ReplicationFactor: 1    Configs: segment.bytes=1073741824
        Topic: atscale  Partition: 0    Leader: 1       Replicas: 1     Isr: 1  Elr:    LastKnownElr:
        Topic: atscale  Partition: 1    Leader: 2       Replicas: 2     Isr: 2  Elr:    LastKnownElr:


```
## 4. 

Use data-generator and send `https://raw.githubusercontent.com/erkansirin78/datasets/master/Churn_Modelling.csv` to  3 partitioned `churn` topic.


- Message key should be CustomerId.

- Consume under `churn_group` and this group must have 3 consumer. 
    - Use different terminal for each consumer. 
    - Use `kafka-console-consumer.sh` as a consumer.

```
root@0e1e0b5ab6af:/data-generator# python3 dataframe_to_kafka.py   -i input/Churn_Modelling.csv   -t churn   -k 0   -b localhost:9092   -rst 0.1
input: input/Churn_Modelling.csv
sep: ,
kafka_sep: ,
row_sleep_time: 0.1
repeat: 1
shuffle: False
self.excluded_cols: ['it_is_impossible_column']
columns_to_write ['RowNumber', 'CustomerId', 'Surname', 'CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Exited']
topic: churn
key_index: 0
bootstrap_servers: ['localhost:9092']
0 - 1,15634602,Hargrave,619,France,Female,42,2,0.0,1,1,1,101348.88,1
1/10000 processed, % 99.99 will be completed in 16.66 mins.
1 - 2,15647311,Hill,608,Spain,Female,41,1,83807.86,1,0,1,112542.58,0
2/10000 processed, % 99.98 will be completed in 16.66 mins.
2 - 3,15619304,Onio,502,France,Female,42,8,159660.8,3,1,0,113931.57,1
3/10000 processed, % 99.97 will be completed in 16.66 mins.
3 - 4,15701354,Boni,699,France,Female,39,1,0.0,2,0,0,93826.63,0
4/10000 processed, % 99.96 will be completed in 16.66 mins.
4 - 5,15737888,Mitchell,850,Spain,Female,43,2,125510.82,1,1,1,79084.1,0
5/10000 processed, % 99.95 will be completed in 16.66 mins.
5 - 6,15574012,Chu,645,Spain,Male,44,8,113755.78,2,1,0,149756.71,1
6/10000 processed, % 99.94 will be completed in 16.66 mins.
6 - 7,15592531,Bartlett,822,France,Male,50,7,0.0,2,1,1,10062.8,0
7/10000 processed, % 99.93 will be completed in 16.65 mins.
7 - 8,15656148,Obinna,376,Germany,Female,29,4,115046.74,4,1,0,119346.88,1
8/10000 processed, % 99.92 will be completed in 16.65 mins.
```


```
root@0e1e0b5ab6af:/# /kafka/bin/kafka-consumer-groups.sh   --bootstrap-server localhost:9092   --describe   --group churn_group

GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID                                           HOST            CLIENT-ID
churn_group     churn           1          1041            1050            9               console-consumer-bb96a134-e9ef-4fb0-9d08-480d7e2bd9e3 /172.18.0.12    console-consumer
churn_group     churn           0          1119            1131            12              console-consumer-7cf96502-6bd5-4b45-b873-8bea5f69fa11 /172.18.0.11    console-consumer
churn_group     churn           2          1003            1013            10              console-consumer-e8983ec4-761e-41c5-9e6d-609bacd3ff57 /172.18.0.11    console-consumerroot@0e1e0b5ab6af:/#
```


## 5. 
Delete `atscale` and `churn` topics

```
root@0e1e0b5ab6af:/# /kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic atscale

root@0e1e0b5ab6af:/# /kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic churn
root@0e1e0b5ab6af:/# /kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
__consumer_offsets
_schemas
root@0e1e0b5ab6af:/#
```