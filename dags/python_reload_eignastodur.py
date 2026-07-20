from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timedelta
import os

from assets import verdbref_ready, eignastodur_ready

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='run_reload_eignastodur',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    # Reads am.verdbref / am.verdbrhreyf, both fresh once the merge asset fires.
    schedule=[verdbref_ready],
    catchup=False,
    description='Reload am.eignastodur_daglegt (EXEC am.usp_hlada_eignastodur_daglegt)',
) as dag:

    reload_table = DockerOperator(
        task_id='reload_eignastodur_daglegt',
        image='python-ubuntu',
        api_version='auto',
        auto_remove="success",
        command='/app/scripts/checks/reload_eignastodur_daglegt.py',
        # Full-history TRUNCATE + INSERT rebuild; give it room.
        execution_timeout=timedelta(minutes=60),
        # Fire the asset so the return-quality check runs on the fresh table.
        outlets=[eignastodur_ready],
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

    reload_table >> notify_failure
