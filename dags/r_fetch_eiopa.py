from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime
import os

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='run_r_fetch_eiopa',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule="0 8 4-8 * *",
    catchup=False,
    description='Fetch EIOPA Yield Curves',
) as dag:

    run_r_script = DockerOperator(
        task_id='fetch_eiopa',
        image='r-ubuntu',
        api_version='auto',
        auto_remove="success",
        command='/app/scripts/fetch_eiopa.R',
        network_mode='bridge',
        mounts=[
            Mount(source='/home/sl-ragnar/airflow/r_scripts', target='/app/scripts', type='bind')
        ], mount_tmp_dir=False,
            tmp_dir="/tmp/airflow", 
            environment={
            "DB_USER": os.environ.get("DB_USER", "placeholder"),
            "DB_USER_PW": os.environ.get("DB_USER_PW", "placeholder"),
            "DB_SERVER": os.environ.get("DB_SERVER", "localhost"),
            "DB_NAME": os.environ.get("DB_NAME", "defaultdb"),
        }
    ) 