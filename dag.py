from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from pre_processing import pre_process

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

    pre_process = PythonOperator(
        task_id="pre_process",
        python_callable=pre_process,
    )


check_file >> pre_process
#docker-compose -f .\docker-compose-LocalExecutor.yml down