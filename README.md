### Airflow
- Orchestrator, not a data processing framework. Process your gigabytes of data outside of Airflow (i.e. Spark cluster, use an operator to execute a Spark job, and the data is processed in Spark).
- A DAG is a data pipeline, an Operator is a task.
- An Executor defines how your tasks are executed, whereas a worker is a process executing your task
- The Scheduler schedules your tasks, the web server serves the UI, and the database stores the metadata of Airflow.

### Components
- Web Server
    - Provides Airflow UI - View, Manage & Monitor Workflows 
- Scheduler
    - Schedule the task
- Meta Database
    - Stores information related to tasks and it's status
- Trigger
    - Relatime events - tasks that trigger by external events
- Executor
    - Determines how your tasks will be run i.e. in sequence or paraller also which node
- Queue
    - Is a list of tasks waiting to be executed. It fetch task from executor and manage task execution order when there are many tasks to run
- Worker
    - Processes that performs the task, pull tasks from the queue

### Concept
- DAG
    - Directed Acyclic Graph 
    - Define structure of workflow showing which tasks execution order and dependencies
- Operator
    - Single idempotent tasks in DAG or one task in our data pipeline
    - 
    - Types 
        - Action Operator: Execute an action i.e.
            - Python Operator - execute python scripts
            - Bash Operator - execute bash scripts
            - SqlExecuteQueryOperator - execute sql queries
        - Transfer Operator: Transfer Data
        - Sensor: Wait for a condition to trigger
            - FileSensor - wait for file
    - Installing Operators
        - Airflow core : _pip install apache-airflow_
        - AWS : _pip install apache-airflow-providers-amazon_
        - Databricks : _pip install apache-airflow-providers-databricks_
        - Snowflake : _pip install apache-airflow-providers-snowflake_
        - Dbt : _pip install apache-airflow-providers-dbt-cloud_
- Task/ Task Instance
    - Specific instance of an operator
    - when operator assigned to a DAG it becomes a task
- Workflow
    - entire process defined in the DAG including task and dependencies
 
### Setup
- Single node architecture
    - standalone server
    - all components of airflow running on a single instanse
- Multi node architecture
    - airflow running on multiple servers
    - components of airflow running on a multiple instanse

### How it works
- add file to __dag__ folder
- __scheduler__ scan __dag__ folder, read any new file, parse and store it in __meta store__ as __dag run__
- __scheduler__ sends __dag run__ task as __task instance__ to __executor__
- __worker__ then fetches this __task instance__ from __executor__ via __queue__ and update the status in __meta store__

### Datasets
- Dataset is a trigger that initiates a DAG run based on a file/table update by another DAG
- DAGs can only use Datasets in the same Airflow instance. A DAG cannot wait for a Dataset defined in another Airflow instance.
- Consumer DAGs are triggered every time a task that updates datasets completes successfully. Airflow doesn't check whether the data has been effectively updated.
- We can't combine different schedules like datasets with cron expressions.
- If two tasks update the same dataset, as soon as one is done, that triggers the Consumer DAG immediately without waiting for the second task to complete.
- Airflow monitors datasets only within the context of DAGs and Tasks. If an external tool updates the actual data represented by a Dataset, Airflow has no way of knowing that.