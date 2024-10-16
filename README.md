### Airflow
- etl orchestration create tasks, execute tasks
- ensure each task starts only once previous task completes
- scheduler
- task can be simple db queries or complex tasks like training AI models, checking data quality, etc...

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
    - Single idempotent tasks in DAG
    - Types 
        - Python Operator - execute python scripts
        - Bash Operator - execute bash scripts
        - SqlExecuteQueryOperator - execute sql queries
        - FileSensor - wait for file
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
