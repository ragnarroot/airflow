from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timedelta
import os

from assets import eignastodur_ready

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='run_check_return_quality',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    # Runs after am.eignastodur_daglegt has been reloaded.
    schedule=[eignastodur_ready],
    catchup=False,
    description='Scan am.eignastodur_daglegt for return-calculation data issues',
) as dag:

    run_check = DockerOperator(
        task_id='check_return_quality',
        image='python-ubuntu',
        api_version='auto',
        auto_remove="success",
        # --fetch forces the DB path (reads the freshly reloaded table) instead
        # of any stale local/dashboard parquet cache.
        command='/app/scripts/checks/check_return_quality.py --fetch',
        execution_timeout=timedelta(minutes=30),
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
            "OUTLOOK_EMAIL": os.environ.get("OUTLOOK_EMAIL", "localhost"),
        }
    )

    notify_failure = DockerOperator(
        task_id='notify_failure',
        image='python-ubuntu',
        api_version='auto',
        auto_remove="success",
        command='/app/scripts/checks/notify_dag_failure.py',
        trigger_rule="one_failed",
        network_mode='bridge',
        mounts=[
            Mount(source='/home/sl-ragnar/airflow/python_scripts', target='/app/scripts', type='bind')
        ], mount_tmp_dir=False,
            tmp_dir="/tmp/airflow",
            environment={
            "AZURE_TENANT_ID": os.environ.get("AZURE_TENANT_ID", "placeholder"),
            "AZURE_CLIENT_ID": os.environ.get("AZURE_CLIENT_ID", "placeholder"),
            "AZURE_CLIENT_SECRET": os.environ.get("AZURE_CLIENT_SECRET", "localhost"),
            "OUTLOOK_EMAIL": os.environ.get("OUTLOOK_EMAIL", "localhost"),
            "AIRFLOW_DAG_ID": "{{ dag.dag_id }}",
            "AIRFLOW_RUN_ID": "{{ run_id }}",
            "AIRFLOW_LOGICAL_DATE": "{{ ts }}",
        }
    )

    run_check >> notify_failure
