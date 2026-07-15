from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime
import os

from assets import verdbref_ready

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='run_check_sl_fjarstefna',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule=[verdbref_ready],
    catchup=False,
    description='Check if fjarfestingarstefna is ok',
) as dag:

    run_python_script = DockerOperator(
        task_id='check_if_fjarfestingar_ok',
        image='python-ubuntu',
        api_version='auto',
        auto_remove="success",
        command='/app/scripts/checks/sl_fjarfestingar_hlutfoll_check.py',
        network_mode='bridge',
        mounts=[
            Mount(source='/home/sl-ragnar/airflow/python_scripts', target='/app/scripts', type='bind')
        ], mount_tmp_dir=False,
            tmp_dir="/tmp/airflow", 
            environment={
            "DB_USER": os.environ.get("DB_USER", "placeholder"),
            "DB_USER_PW": os.environ.get("DB_USER_PW", "placeholder"),
            "DB_SERVER": os.environ.get("DB_SERVER", "localhost"),
            "DB_NAME": os.environ.get("DB_NAME", "defaultdb"),
            "AZURE_TENANT_ID": os.environ.get("AZURE_TENANT_ID", "placeholder"),
            "AZURE_CLIENT_ID": os.environ.get("AZURE_CLIENT_ID", "placeholder"),
            "AZURE_CLIENT_SECRET": os.environ.get("AZURE_CLIENT_SECRET", "localhost"),
            "OUTLOOK_EMAIL": os.environ.get("OUTLOOK_EMAIL", "localhost")
        }
    ) 