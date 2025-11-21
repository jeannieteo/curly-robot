from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# DAG configuration
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['cloversoftie@gmail.com'],
    'retries': 1,
    'execution_timeout': timedelta(minutes=20),
}

dag = DAG(
    'pyspark_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline using PySpark',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
)

# Step 1: Run PySpark job
spark_task = BashOperator(
    task_id="run_pyspark_etl",
    bash_command="""
        spark-submit \
        --master local[*] \
	--packages org.apache.hadoop:hadoop-aws:3.3.4 \
  	--conf spark.hadoop.fs.s3a.access.key=$AWS_ACCESS_KEY_ID \
  	--conf spark.hadoop.fs.s3a.secret.key=$AWS_SECRET_ACCESS_KEY \
  	--conf spark.hadoop.fs.s3a.endpoint=s3.ap-southeast-2.amazonaws.com \
        /opt/airflow/dags/scripts/pyspark_etl.py
    """,
    dag=dag,
)

# Step 2: Validate output
validate_task = BashOperator(
    task_id='validate_output',
    bash_command='python /opt/airflow/dags/scripts/validate.py',
    dag=dag,
)


# Task dependencies
spark_task >> validate_task