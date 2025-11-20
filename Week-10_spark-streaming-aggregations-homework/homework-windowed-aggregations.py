from pyspark.sql import SparkSession, functions as F

accessKeyId = 'dataops'
secretAccessKey = 'Ankara06'
bucket_name = "datasets"
stream_source_directory = "/iot_stream_input"

checkpointDir = f"s3a://{bucket_name}/checkpoint/iot_windowed_agg"

spark = (
    SparkSession.builder
    .appName("IoT Windowed Aggregations 10min")
    .config("spark.hadoop.fs.s3a.access.key", accessKeyId)
    .config("spark.hadoop.fs.s3a.secret.key", secretAccessKey)
    .config("spark.hadoop.fs.s3a.path.style.access", True)
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

iot_schema = (
    "ts double, "
    "device string, "
    "humidity double, "
    "flag1 string, "
    "co double, "
    "flag2 string, "
    "smoke double, "
    "temp double, "
    "event_time string"
)

lines = (
    spark.readStream
    .format("csv")
    .schema(iot_schema)
    .option("header", False)
    .load(f"s3a://{bucket_name}{stream_source_directory}")
)


lines_with_time = lines.withColumn(
    "event_time_ts",
    F.to_timestamp(F.col("event_time"))
)

windowedAgg = (
    lines_with_time
    .groupBy(
        F.window(F.col("event_time_ts"), "10 minutes", "5 minutes"),
        F.col("device")
    )
    .agg(
        F.count("*").alias("signal_count"),
        F.avg("co").alias("avg_co"),
        F.avg("humidity").alias("avg_humidity")
    )
    .orderBy("window")
)

streamingQuery = (
    windowedAgg.writeStream
    .format("console")
    .outputMode("complete")
    .trigger(processingTime="5 second")
    .option("checkpointLocation", checkpointDir)
    .option("numRows", 30)
    .option("truncate", False)
    .start()
)

streamingQuery.awaitTermination()

