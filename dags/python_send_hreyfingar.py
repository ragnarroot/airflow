# from airflow import DAG
# from airflow.providers.docker.operators.docker import DockerOperator
# from docker.types import Mount
# from datetime import datetime
# import os

# default_args = {
#     'owner': 'airflow',
# }

# with DAG(
#     dag_id='run_send_verdbrhreyf',
#     default_args=default_args,
#     start_date=datetime(2026, 3, 13),
#     schedule="0 9 * * *",
#     catchup=False,
#     description='keep track of changes in joakim verdbref',
# ) as dag:

#     send_verdbrhreyf = DockerOperator(
#         task_id='send_verdbrhreyf',
#         image='python-ubuntu',
#         api_version='auto',
#         auto_remove="success",
#         command='/app/scripts/checks/send_new_investment_movement.py',
#         network_mode='bridge',
#         mounts=[
#             Mount(source='/home/sl-ragnar/airflow/python_scripts', target='/app/scripts', type='bind')
#         ], mount_tmp_dir=False,
#             tmp_dir="/tmp/airflow", 
#             environment={
#             "DB_USER": os.environ.get("DB_USER", "placeholder"),
#             "DB_USER_PW": os.environ.get("DB_USER_PW", "placeholder"),
#             "DB_SERVER": os.environ.get("DB_SERVER", "localhost"),
#             "DB_NAME": os.environ.get("DB_NAME", "defaultdb"),
#             "BC_TENANT_ID": os.environ.get("BC_TENANT_ID", "placeholder"),
#             "BC_CLIENT_ID": os.environ.get("BC_CLIENT_ID", "placeholder"),
#             "BC_CLIENT_SECRET": os.environ.get("BC_CLIENT_SECRET", "localhost"),
#             "BC_COMPANY_ID": os.environ.get("BC_COMPANY_ID", "defaultdb"),
#             "AZURE_TENANT_ID": os.environ.get("AZURE_TENANT_ID", "placeholder"),
#             "AZURE_CLIENT_ID": os.environ.get("AZURE_CLIENT_ID", "placeholder"),
#             "AZURE_CLIENT_SECRET": os.environ.get("AZURE_CLIENT_SECRET", "localhost"),
#             "OUTLOOK_EMAIL": os.environ.get("OUTLOOK_EMAIL", "localhost"),
#         }
#     ) 
