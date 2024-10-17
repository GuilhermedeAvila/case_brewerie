## Case_brewerie

Overview
This project is designed to retrieve data from the Open Brewery DB API, process it using Docker, Apache Airflow and Databricks, and store it in AWS S3 buckets following a structured data pipeline.

Project Tools and Challenges
For this project, I utilized Docker, Apache Airflow, and Databricks. Although I had no prior experience with Airflow and Docker, I gained valuable knowledge while working on this case and successfully demonstrated some of my core skills.

Key Steps:
Databricks and PySpark: I set up a Databricks cluster with PySpark, configured my AWS credentials, and established a connection to AWS S3 storage. I created three notebooks to handle different stages of the ETL process:

Bronze Layer: Retrieved and ingested raw data into the bronze folder on S3.
Silver Layer: Validated essential columns received from the API and saved the data in Parquet format, partitioned by specified columns.
Gold Layer: Performed final validations on column types and saved the processed data in Parquet, adhering to defined business rules.
Apache Airflow: I used Airflow to orchestrate the pipeline by creating a Directed Acyclic Graph (DAG) to connect tasks that run the Databricks notebooks. I configured the Databricks connection in the Admin > Connections tab within Airflow. Additionally, I implemented email notifications for both success and failure to monitor the pipeline's execution.

How to Run the Solution
To use this solution, follow these steps:

Clone this repository.

Run the following command to start the services using Docker Compose:

bash
docker compose up -d

If an error occurs, it may be due to the use of a customized Airflow image. To resolve this, build the custom image with the necessary Apache Airflow and Databricks libraries by running:

bash
docker build . --tag 'your_custom_image_name'


After building the custom image, update the docker-compose.yaml file to use this custom image.

To connect to Databricks, you will need to create an environment variable file containing the required credentials. If you need assistance with obtaining the credentials for testing, please contact me.

