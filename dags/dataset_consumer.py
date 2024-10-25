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
    dag_id='dataset_consumer',
    schedule=[example_dataset,example_dataset_1,example_dataset_n],
    start_date=datetime(2024,10,24),
    catchup=False):

    @task
    def read_dataset():
        with open(example_dataset.uri, 'r') as f:
            print(f.read())

    read_dataset()