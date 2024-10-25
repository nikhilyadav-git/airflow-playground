from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

example_dataset = Dataset('/tmp/dataset.tx')
example_dataset_1 = Dataset('/tmp/dataset_1.txt')
# .
# .
# .
example_dataset_n = Dataset('/tmp/dataset_n.txt')

with DAG(
    dag_id='dataset_producer',
    schedule='@daily',
    start_date=datetime(2024,10,24),
    catchup=False):
    
    @task(outlets=example_dataset)
    def update_dataset():
        with open(example_dataset.uri, 'a+') as f:
            f.write('producer update')

    @task(outlets=example_dataset_1)
    def update_dataset_1():
        with open(example_dataset_1.uri, 'a+') as f:
            f.write('producer update')

    @task(outlets=example_dataset_n)
    def update_dataset_n():
        with open(example_dataset_n.uri, 'a+') as f:
            f.write('producer update')

    update_dataset() >> update_dataset_1() >> update_dataset_n()