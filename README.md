## curly-robot
### README: PySpark ETL Pipeline with Airflow & Docker
#### Project Overview
This project demonstrates an end-to-end ETL pipeline using PySpark, orchestrated with Apache Airflow, and containerized with Docker. It processes multi-table retail data, performs transformations, and writes results to Parquet (or S3).

#### Architecture
[Data Source: Kaggle CSVs] → [PySpark ETL] → [Airflow DAG] → [Parquet/S3]

#### Prerequisites

- Docker Desktop (with WSL2 backend enabled)
- Git
- AWS credentials for using S3
- Kaggle dataset: https://www.kaggle.com/datasets/joycemara/european-fashion-store-multitable-dataset

#### Project Structure

project-root/
<br>├── Dockerfile
<br> ├── docker-compose.yml
<br> ├── dags/
<br> │    ├── pyspark_etl_dag.py
<br> │    └── scripts/
<br> │         ├── pyspark_etl.py
<br> │         └── validate.py
<br> ├── requirements.txt
<br> └── README.md

### Setup Instructions
- 1. Clone the Repository
git clone https://github.com/your-username/pyspark-airflow-etl.git
cd pyspark-airflow-etl

- 2. Place Your Data
Download the Kaggle dataset and put CSV files in data/ or upload to S3.
AWS S3 buckets contains the csv files:
![S3Buckets](./images/awsS3BucketsCSV.png "S3")

- 3. Build Your Custom Image: files: Dockerfile, docker-compose.yml
<br>`docker build -t airflow-spark-etl .`
<br>`docker-compose build`
![docker build](./images/dockerbuild.png "docker build")
Generate a Fernet Key: Airflow requires a Fernet key for encrypting sensitive data. Generate one using Python:

	from cryptography.fernet import Fernet
	print(Fernet.generate_key().decode())
	Replace YOUR_FERNET_KEY in the docker-compose.yml file with the generated key.

- 4. Initialize the Database: Run the following command to initialize the Airflow database:

`docker-compose run airflow airflow db init`
![docker run](./images/dockerRun.png "docker Run")
- 5. Start Services
`docker-compose up -d`

- 6. Add admin user for login into Airflow UI
`docker-compose run airflow airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com --password admin`
![user](./images/dockerRuncreateuser.png "make user")
- 7. Access Airflow UI
Go to: http://localhost:8080
Default credentials: admin / admin

- 8. Trigger DAG
Enable and trigger pyspark_etl_dag in Airflow UI.
![airflow1](./images/airflow1.png "airflow1")

#### Airflow DAG Overview
<br>Task 1: Run PySpark ETL (spark-submit inside container).
<br>Task 2: Validate output using validate.py.


#### Environment Variables
<br>Set AWS credentials in .env or Docker Compose:
<br>AWS_ACCESS_KEY_ID=your_key
<br>AWS_SECRET_ACCESS_KEY=your_secret
<br>AWS_DEFAULT_REGION=your_region


#### Tech Stack
<br>Apache Airflow for orchestration
<br>PySpark for ETL
<br>Docker & Docker Compose for containerization
<br>Postgres for Airflow metadata
<br>AWS S3 (optional) for storage

-----------------------------------------

Local execution on windows always breaks

spark-submit  --master local[*] --packages org.apache.hadoop:hadoop-aws:3.4.1   --conf spark.hadoop.fs.s3a.access.key=<AWS_KEY_ID> --conf spark.hadoop.fs.s3a.secret.key=<AWS_SECRET_KEY> --conf spark.hadoop.fs.s3a.endpoint=s3.amazonaws.com   pyspark_etl.py
