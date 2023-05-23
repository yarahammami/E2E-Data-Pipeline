from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.mysql import MySqlOperator
from pre_processing import pre_process
from pre_process import process_data


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

    aggregation = PythonOperator(
        task_id="aggregation",
        python_callable=process_data,
    )

    create_table = MySqlOperator(
        task_id="create_table",
        mysql_conn_id="mysql_db1",
        sql = "CREATE table IF NOT EXISTS aggre_res (stock_code varchar(100) NULL,descb varchar(100) NULL,country varchar(100) NULL,total_price varchar(100) NULL)"
    )

    insert = MySqlOperator(
        task_id='insert_db',
        mysql_conn_id="mysql_db1",
        sql="LOAD DATA  INFILE '/var/lib/mysql-files/fin.csv' INTO TABLE aggre_res FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;")



check_file >> pre_process >> aggregation
#docker-compose -f .\docker-compose-LocalExecutor.yml down