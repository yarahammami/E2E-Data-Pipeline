from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 5, 18)
}
with DAG(dag_id="workflow", default_args=default_args, schedule_interval='@daily') as dag:
    check_file = BashOperator(
        task_id="check_file",
        bash_command="shashum ~/ip_files/or.csv",
        retries=2,
        retry_delay=timedelta(seconds=15)
    )