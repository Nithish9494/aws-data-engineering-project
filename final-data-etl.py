import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1710444729122 = glueContext.create_dynamic_frame.from_catalog(database="db_youtube_cleaned", table_name="cleaned_statistics_reference_data", transformation_ctx="AWSGlueDataCatalog_node1710444729122")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1710444764426 = glueContext.create_dynamic_frame.from_catalog(database="db_youtube_cleaned", table_name="raw_statistics", transformation_ctx="AWSGlueDataCatalog_node1710444764426")

# Script generated for node Join
Join_node1710444892603 = Join.apply(frame1=AWSGlueDataCatalog_node1710444764426, frame2=AWSGlueDataCatalog_node1710444729122, keys1=["category_id"], keys2=["id"], transformation_ctx="Join_node1710444892603")

# Script generated for node Amazon S3
AmazonS3_node1710460194373 = glueContext.getSink(path="s3://dev-youtube-analytics", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=["region", "category_id"], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1710460194373")
AmazonS3_node1710460194373.setCatalogInfo(catalogDatabase="db_youtube_analytics",catalogTableName="finaly_analytics")
AmazonS3_node1710460194373.setFormat("glueparquet", compression="snappy")
AmazonS3_node1710460194373.writeFrame(Join_node1710444892603)
job.commit()
