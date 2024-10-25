# import DAG
from airflow import DAG

# import operators
# postgresql provider operator
from airflow.providers.postgres.operators.postgres import PostgresOperator
# postgresql hook - hook is abstraction layer on top of operator to simplify the tasks
from airflow.providers.postgres.hooks.postgres import PostgresHook  
# http provider operator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
# python operator
from airflow.operators.python import PythonOperator

#pandas
from pandas import json_normalize

#python libs
from datetime import datetime
import json
import logging

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Check if the logger already has handlers
if not logger.handlers:
    # Create handlers
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('/tmp/processesd_user.log')

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

# define functions
def _processes_user_fn(ti):
    try:
        user = ti.xcom_pull(task_ids='extract_user')
        user = user['results'][0]
        processesd_user = json_normalize({
            'firstname': user['name']['first'],
            'lastname': user['name']['last'],
            'country': user['location']['country'],
            'username': user['login']['username'],
            'password': user['login']['password'],
            'email': user['email']
        })
        logger.info(f"processesd_user: {processesd_user}")
        processesd_user.to_csv('/tmp/processesd_user.csv', index=None, header=False)
    except Exception as e:
        logger.error(f"Function _processes_user_fn failed to create csv, exception details: {e}")

def _store_user_fn():
    try:
        hook = PostgresHook(
            postgres_conn_id='postgres_connection')
        hook.copy_expert(
            sql="copy users from stdin with delimiter as ','",
            filename='/tmp/processesd_user.csv'
            )
    except Exception as e:
        logger.error(f"Function _store_user_fn failed to update csv in db, exception details: {e}")

# initiate a DAG
with DAG('user_processing', 
         start_date=datetime(2024,1,1),
         schedule_interval='@daily',
         catchup=False) as dag:
    # action operator - postgres
    logger.info("Task 'create_table' strated!")
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_connection',
        sql='''Create table if not exists users (firstname text,
        lastname text, country text, username text, password text, 
        email text)'''
    )
    logger.info("Task 'create_table' finished!")

    # sensor operator - http
    logger.info("Task 'is_api_available' strated!")
    is_api_available = HttpSensor(
        task_id = 'is_api_available', 
        http_conn_id = 'user_api',
        endpoint = 'api/'
    )
    logger.info("Task 'is_api_available' finished!")

    # action operator - http
    logger.info("Task 'extract_user' strated!")
    extract_user = SimpleHttpOperator(
        task_id = 'extract_user',
        http_conn_id = 'user_api',
        endpoint = 'api/',
        method = 'GET',
        response_filter = lambda response: json.loads(response.text),
        log_response = True
    )
    logger.info("Task 'extract_user' finished!")

    # action operator - python
    logger.info("Task 'processes_user' strated!")
    processes_user = PythonOperator(
        task_id = 'processes_user',
        python_callable=_processes_user_fn
    )
    logger.info("Task 'processes_user' finished!")

    # action operator - python
    logger.info("Task 'store_user' strated!")
    store_user = PythonOperator(
        task_id = 'store_user',
        python_callable=_store_user_fn
    )
    logger.info("Task 'store_user' finished!")

    # Define DAG
    create_table >> is_api_available >> extract_user >> processes_user >> store_user