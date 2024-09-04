from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

def run_youtube_script():
    # Assuming the script is named youtube_fetcher.py and located in the same directory
    import subprocess
    subprocess.run(['python', '/Users/nouhailanigrou/Desktop/youtube/python.py'])

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 31),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'youtube_data_fetcher',
    default_args=default_args,
    description='A DAG to fetch YouTube data and send to Kafka',
    schedule_interval=timedelta(minutes=10),  # Adjust as needed
)

fetch_data_task = PythonOperator(
    task_id='fetch_youtube_data',
    python_callable=run_youtube_script,
    dag=dag,
)

