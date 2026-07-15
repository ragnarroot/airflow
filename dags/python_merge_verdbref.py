from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timedelta
import os

from assets import verdbref_ready

default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='run_merge_verdbref',
    default_args=default_args,
    start_date=datetime(2023, 1, 1),
    schedule="0 9 * * *",
    catchup=False,
    description='keep track of changes in joakim verdbref',
) as dag:

    run_python_script = DockerOperator(
        task_id='merge_verdbref',
        image='python-ubuntu',
        api_version='auto',
        auto_remove="success",
        command='/app/scripts/merge_verdbref.py',
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
            "BC_TENANT_ID": os.environ.get("BC_TENANT_ID", "placeholder"),
            "BC_CLIENT_ID": os.environ.get("BC_CLIENT_ID", "placeholder"),
            "BC_CLIENT_SECRET": os.environ.get("BC_CLIENT_SECRET", "localhost"),
            "BC_COMPANY_ID": os.environ.get("BC_COMPANY_ID", "defaultdb"),
        }
    ) 

    run_check_script = DockerOperator(
        task_id='check_merge_verdbref',
        image='python-ubuntu',
        api_version='auto',
        auto_remove="success",
        command='/app/scripts/checks/check_merge_verdbref.py',
        execution_timeout=timedelta(minutes=15),
        outlets=[verdbref_ready],
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
            "BC_TENANT_ID": os.environ.get("BC_TENANT_ID", "placeholder"),
            "BC_CLIENT_ID": os.environ.get("BC_CLIENT_ID", "placeholder"),
            "BC_CLIENT_SECRET": os.environ.get("BC_CLIENT_SECRET", "localhost"),
            "BC_COMPANY_ID": os.environ.get("BC_COMPANY_ID", "defaultdb"),
            "AZURE_TENANT_ID": os.environ.get("AZURE_TENANT_ID", "placeholder"),
            "AZURE_CLIENT_ID": os.environ.get("AZURE_CLIENT_ID", "placeholder"),
            "AZURE_CLIENT_SECRET": os.environ.get("AZURE_CLIENT_SECRET", "localhost"),
            "OUTLOOK_EMAIL": os.environ.get("OUTLOOK_EMAIL", "localhost"),
        }
    ) 





    run_merge_verdbrhreyf = DockerOperator(
        task_id='merge_verdbrefhreyf',
        image='python-ubuntu',
        api_version='auto',
        auto_remove="success",
        command='/app/scripts/merge_verdbrhreyf.py',
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
            "BC_TENANT_ID": os.environ.get("BC_TENANT_ID", "placeholder"),
            "BC_CLIENT_ID": os.environ.get("BC_CLIENT_ID", "placeholder"),
            "BC_CLIENT_SECRET": os.environ.get("BC_CLIENT_SECRET", "localhost"),
            "BC_COMPANY_ID": os.environ.get("BC_COMPANY_ID", "defaultdb"),
        }
    ) 

    run_check_merge_verdbrhreyf = DockerOperator(
        task_id='check_merge_verdbrhreyf',
        image='python-ubuntu',
        api_version='auto',
        auto_remove="success",
        command='/app/scripts/checks/check_merge_verdbrhreyf.py',
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
            "BC_TENANT_ID": os.environ.get("BC_TENANT_ID", "placeholder"),
            "BC_CLIENT_ID": os.environ.get("BC_CLIENT_ID", "placeholder"),
            "BC_CLIENT_SECRET": os.environ.get("BC_CLIENT_SECRET", "localhost"),
            "BC_COMPANY_ID": os.environ.get("BC_COMPANY_ID", "defaultdb"),
            "AZURE_TENANT_ID": os.environ.get("AZURE_TENANT_ID", "placeholder"),
            "AZURE_CLIENT_ID": os.environ.get("AZURE_CLIENT_ID", "placeholder"),
            "AZURE_CLIENT_SECRET": os.environ.get("AZURE_CLIENT_SECRET", "localhost"),
            "OUTLOOK_EMAIL": os.environ.get("OUTLOOK_EMAIL", "localhost"),
        }
    ) 


    send_verdbrhreyf = DockerOperator(
        task_id='send_verdbrhreyf',
        image='python-ubuntu',
        api_version='auto',
        auto_remove="success",
        command='/app/scripts/checks/send_new_investment_movement.py',
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
            "BC_TENANT_ID": os.environ.get("BC_TENANT_ID", "placeholder"),
            "BC_CLIENT_ID": os.environ.get("BC_CLIENT_ID", "placeholder"),
            "BC_CLIENT_SECRET": os.environ.get("BC_CLIENT_SECRET", "localhost"),
            "BC_COMPANY_ID": os.environ.get("BC_COMPANY_ID", "defaultdb"),
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

    run_python_script >> run_check_script
    run_merge_verdbrhreyf >> run_check_merge_verdbrhreyf >> send_verdbrhreyf

    # Alert if the run does not finish. notify_failure is a direct child of every
    # task that can fail, so a real "failed" state is always its own parent
    # (one_failed counts failed parents, not upstream_failed ones). It is skipped
    # on a fully successful run.
    [
        run_python_script,
        run_check_script,
        run_merge_verdbrhreyf,
        run_check_merge_verdbrhreyf,
        send_verdbrhreyf,
    ] >> notify_failure