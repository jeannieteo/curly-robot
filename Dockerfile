FROM apache/airflow:2.8.1-python3.11

USER root

# Install dependencies
RUN apt-get update && apt-get install -y wget curl unzip && apt-get clean

# Install OpenJDK 11 from Adoptium
RUN wget https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.22+7/OpenJDK11U-jdk_x64_linux_hotspot_11.0.22_7.tar.gz && \
    tar -xvf OpenJDK11U-jdk_x64_linux_hotspot_11.0.22_7.tar.gz && \
    mv jdk-11.0.22+7 /usr/local/openjdk-11 && \
    rm OpenJDK11U-jdk_x64_linux_hotspot_11.0.22_7.tar.gz

# Set JAVA_HOME
ENV JAVA_HOME=/usr/local/openjdk-11
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Spark
ENV SPARK_VERSION=3.5.7
ENV HADOOP_VERSION=3
RUN wget https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar xvf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Set Spark environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Add Hadoop AWS connector for S3
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar -P $SPARK_HOME/jars && \
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar -P $SPARK_HOME/jars

USER airflow
ENV AIRFLOW_HOME=/opt/airflow

# Copy DAGs and scripts
COPY dags/ $AIRFLOW_HOME/dags/

# Install Python dependencies
RUN pip install pyspark boto3

# Restore the default entrypoint and command
ENTRYPOINT ["/usr/bin/dumb-init", "--", "/entrypoint"]
CMD ["webserver"]
