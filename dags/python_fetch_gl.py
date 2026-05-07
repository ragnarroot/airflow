from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime
import os

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='run_python_fetch_gl',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule="0 8 * * *",
    catchup=False,
    description='Fetch new ids from the general ledger',
) as dag:

    run_r_script = DockerOperator(
        task_id='fetch_GL',
        image='python-ubuntu',
        api_version='auto',
        auto_remove="success",
        command='/scripts/run/upload_gl.py',
        network_mode='bridge',
        mounts=[
            Mount(source='/home/sl-ragnar/airflow/python_scripts', target='/scripts', type='bind')
        ], mount_tmp_dir=False,
            tmp_dir="/tmp/airflow", 
            environment={
            "DB_USER": os.environ.get("DB_USER", "placeholder"),
            "DB_USER_PW": os.environ.get("DB_USER_PW", "placeholder"),
            "DB_SERVER": os.environ.get("DB_SERVER", "localhost"),
            "DB_NAME": os.environ.get("DB_NAME", "defaultdb"),
            "BC_TENANT_ID": os.environ.get("BC_TENANT_ID", "placeholder"),
            "BC_CLIENT_ID": os.environ.get("BC_CLIENT_ID", "placeholder"),
            "BC_CLIENT_SECRET": os.environ.get("BC_CLIENT_SECRET", "localhost"),
            "BC_COMPANY_ID": os.environ.get("BC_COMPANY_ID", "defaultdb"),
        }
    ) 