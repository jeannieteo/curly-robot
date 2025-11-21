from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, countDistinct

# Initialize Spark Session
import os
#os.environ['PYSPARK_PYTHON'] = "C:\Users\User\AppData\Local\Programs\Python\Python313"
#os.environ['PYSPARK_DRIVER_PYTHON'] = "C:\Users\User\AppData\Local\Programs\Python\Python313"
spark = SparkSession.builder \
    .appName("EuropeanFashionStoreETL") \
    .getOrCreate()

# Paths (adjust for your environment)
CUSTOMERS_PATH = "s3a://bucketjtproject/EcommerceEuropeanFashion/dataset_fashion_store_customers.csv"
SALESITEMS_PATH = "s3a://bucketjtproject/EcommerceEuropeanFashion/dataset_fashion_store_salesitems.csv"
SALES_PATH = "s3a://bucketjtproject/EcommerceEuropeanFashion/dataset_fashion_store_sales.csv"
PRODUCTS_PATH = "s3a://bucketjtproject/EcommerceEuropeanFashion/dataset_fashion_store_products.csv"
OUTPUT_PATH = "s3a://bucketjtproject/EcommerceEuropeanFashion/processed/fashion_store/"

# Step 1: Load raw data
customers_df = spark.read.option("header", True).option("inferSchema", "true").csv(CUSTOMERS_PATH)       
salesitems_df = spark.read.option("header", True).option("inferSchema", "true").csv(SALESITEMS_PATH)
sales_df = spark.read.option("header", True).option("inferSchema", "true").csv(SALES_PATH)
products_df = spark.read.option("header", True).option("inferSchema", "true").csv(PRODUCTS_PATH)

# Step 2: Data Cleaning
# Example: Fill null values and enforce schema
salesitems_df = salesitems_df.withColumn("quantity", col("quantity").cast("int")) \
                     .withColumn("unit_price", col("unit_price").cast("double")) \
                     .fillna({"quantity": 0, "unit_price": 0.0})

# Step 3: Join tables
sales_full_df = salesitems_df.join(sales_df, on="sale_id", how="inner")
sales_products_df = sales_full_df.join(products_df, on="product_id", how="inner")
full_df = sales_products_df.join(customers_df, on="customer_id", how="inner")

# Step 4: Transformations
# Calculate revenue per category and country
agg_df = full_df.groupBy("category", "country") \
    .agg(
        _sum(col("quantity") * col("unit_price")).alias("total_revenue"),
        countDistinct("customer_id").alias("unique_customers")
    )

# Step 5: Partition and write to Parquet
agg_df.write \
    .mode("overwrite") \
    .partitionBy("country") \
    .parquet(OUTPUT_PATH)

print("ETL pipeline completed successfully!")