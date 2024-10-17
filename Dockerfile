from apache/airflow:2.10.2-python3.12

USER airflow

RUN pip install apache-airflow apache-airflow-providers-apache-spark apache-airflow-providers-databricks