
  
  CREATE EXTERNAL TABLE `curated_nyx_taxi`(
  `vendorid` bigint, 
  `pickup_datetime` timestamp, 
  `dropoff_datetime` timestamp, 
  `passenger_count` double, 
  `trip_distance` double, 
  `ratecodeid` double, 
  `store_and_fwd_flag` string, 
  `pulocationid` bigint, 
  `dolocationid` bigint, 
  `payment_type` bigint, 
  `fare_amount` double, 
  `extra` double, 
  `mta_tax` double, 
  `tip_amount` double, 
  `tolls_amount` double, 
  `improvement_surcharge` double, 
  `total_amount` double, 
  `congestion_surcharge` double, 
  `airport_fee` double)
PARTITIONED BY ( 
  `pickup_date` date)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://{your_bucket}/tripdata_output/'
