import sys
from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder.appName("DataValidation").getOrCreate()

# Path to processed data (adjust to your S3 or local path)
OUTPUT_PATH = "s3a://bucketjtproject/EcommerceEuropeanFashion/processed/fashion_store/"

# Load processed data
df = spark.read.parquet(OUTPUT_PATH)

# Basic validation checks
print("=== Data Validation Report ===")

# 1. Row count
row_count = df.count()
print(f"Row count: {row_count}")

# 2. Check for nulls in critical columns
critical_columns = ["category", "country", "total_revenue"]
for col_name in critical_columns:
    null_count = df.filter(df[col_name].isNull()).count()
    print(f"Nulls in {col_name}: {null_count}")

# 3. Check for duplicate rows
duplicate_count = df.groupBy(df.columns).count().filter("count > 1").count()
print(f"Duplicate rows: {duplicate_count}")

# 4. Validate revenue is non-negative
negative_revenue = df.filter(df["total_revenue"] < 0).count()
print(f"Negative revenue rows: {negative_revenue}")

if null_count == 0 and duplicate_count == 0 and negative_revenue == 0:
    print("Validation PASSED ✅")
else:
    print("Validation FAILED ❌")

spark.stop()
