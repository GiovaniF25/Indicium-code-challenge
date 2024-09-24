from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'GIOVANI M FERRARI',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'indicium_data_pipeline',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
)

def extract_data(**kwargs):
    from extract_data import extract_data_task
    extract_data_task()

def load_data(**kwargs):
    from load_data import load_data_task
    load_data_task()

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    provide_context=True,
    dag=dag,
)

extract_task >> load_task
