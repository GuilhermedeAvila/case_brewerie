from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
import smtplib
import os


def send_simple_email(subject,msg):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "guilhermeavila.orlando@gmail.com"
    sender_password = os.getenv('SENDER_PASSWORD')
    recipient_email = "guilhermeavila.orlando@gmail.com"
    assunto = subject
    mensagem = msg
    email_message = f"Subject: {assunto}\n\n{mensagem}"

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, email_message.encode('utf-8'))
        server.quit()
        print("E-mail enviado com sucesso!")

    except Exception as e:

        print(f"Erro ao enviar e-mail: {e}")

def enviar_email_sucesso():
    send_simple_email('ETL_Brewerie Success!', 'O script de ETL - Brewerie foi bem sucedido!')

def enviar_email_falha():
    send_simple_email('ETL_Brewerie Failure!', 'O script de ETL - Brewerie falhou!')


default_args = {
    'owner': 'Guilherme Orlando',
    'start_date': datetime(2024, 10, 15),
    'email_on_failure': False,
    'email_on_retry': False,
    'email': ['guilhermeavila.orlando@gmail.com'],
    'retries': 1,
}

with DAG('ETL_SCRIPT',
         default_args=default_args,
         schedule_interval='0 6 * * *',
         catchup=False) as dag:
    
    bronze = DatabricksSubmitRunOperator(
        task_id='RUN_BRONZE',
        databricks_conn_id='databricks_default',
        json={
            "run_name": "Airflow Databricks Bronze",
            "existing_cluster_id": "1016-024557-e384js3",
            "notebook_task": {
                "notebook_path": "/Workspace/Users/guilhermeavilaorlando@gmail.com/bronze",
                "base_parameters": { 
                "aws_access_key": os.getenv('AWS_ACCESS_KEY_ID'), 
                "aws_access_secret": os.getenv('AWS_SECRET_ACCESS_KEY')
            }
            }
        },
    )

    silver = DatabricksSubmitRunOperator(
        task_id='RUN_SILVER',
        databricks_conn_id='databricks_default',
        json={
            "run_name": "Airflow Databricks Silver",
            "existing_cluster_id": "1016-024557-e384js3",
            "notebook_task": {
                "notebook_path": "/Workspace/Users/guilhermeavilaorlando@gmail.com/silver",
                "base_parameters": { 
                "aws_access_key": os.getenv('AWS_ACCESS_KEY_ID'), 
                "aws_access_secret": os.getenv('AWS_SECRET_ACCESS_KEY')
            }
            }
        },
    )

    gold = DatabricksSubmitRunOperator(
        task_id='RUN_GOLD',
        databricks_conn_id='databricks_default',
        json={
            "run_name": "Airflow Databricks GOLD",
            "existing_cluster_id": "1016-024557-e384js3",
            "notebook_task": {
                "notebook_path": "/Workspace/Users/guilhermeavilaorlando@gmail.com/gold",
                "base_parameters": { 
                "aws_access_key": os.getenv('AWS_ACCESS_KEY_ID'), 
                "aws_access_secret": os.getenv('AWS_SECRET_ACCESS_KEY')
            }
            }
        },
    )

    success_notif = PythonOperator(
        task_id='EMAIL_SUCCESS',
        python_callable=enviar_email_sucesso,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    fail_notif = PythonOperator(
        task_id='EMAIL_FAILURE',
        python_callable=enviar_email_falha,
        trigger_rule=TriggerRule.ONE_FAILED
    )

    bronze >> silver >> gold
    gold >> success_notif  
    [bronze, silver, gold] >> fail_notif 