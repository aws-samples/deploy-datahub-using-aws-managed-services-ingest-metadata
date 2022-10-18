
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql.functions import udf, col
from pyspark.sql.types import IntegerType, StringType
from pyspark.sql import SQLContext
from pyspark.context import SparkContext
from datetime import datetime
from pyspark.sql.session import SparkSession


from pyspark.sql import  Row
import pyspark.sql.functions as F
import pyspark.sql.types as T
import pyspark.sql.window as W

spark = SparkSession.builder.config("spark.extraListeners", "datahub.spark.DatahubSparkListener") \
.config("spark.datahub.rest.server","<GMS_ENDPOINT>") \
.config("spark.datahub.rest.token","<GMS_TOKEN>") \
.config("spark.app.name","datahubbloggluelineage") \
.getOrCreate()

spark.conf.set('spark.sql.sources.partitionOverwriteMode', 'dynamic')
spark.conf.set('hive.exec.dynamic.partition', 'true')
spark.conf.set('hive.exec.dynamic.partition.mode', 'nonstrict')

glueContext = GlueContext(spark.sparkContext)
job = Job(glueContext)

logger = glueContext.get_logger()
logger.info("Job initializied")

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
job.init(args['JOB_NAME'], args)
job_time_string = datetime.now().strftime("%Y%m%d%H%M%S")

landing_table_name = "datahub_nyx_taxi.landing_nyx_taxi"

spark_new_df = spark.sql("select * from "+landing_table_name)
spark_new_df.printSchema()

spark_df_transform = spark_new_df.withColumn("pickup_date",F.to_date("tpep_pickup_datetime"))\
                                 .withColumn("pickup_datetime",F.to_timestamp("tpep_pickup_datetime"))\
                                 .withColumn("dropoff_datetime",F.to_timestamp("tpep_dropoff_datetime"))

spark_df_transform = spark_df_transform.drop("tpep_pickup_datetime","tpep_dropoff_datetime")

target_table_name = 'datahub_nyx_taxi.curated_nyx_taxi'
cols = spark.sql("select * from " + target_table_name+ " where 1=0").columns
spark_df_transform = spark_df_transform.select(cols)
  

spark_df_transform.write.mode("overwrite").insertInto(target_table_name)
job.commit()