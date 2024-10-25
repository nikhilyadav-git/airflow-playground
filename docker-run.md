- package entire airflow application, code and libs it need into a single unit/container - docker-compose.yaml
- start and attach containers for airflow service from docker-compose.yml in detach mode i.e. in background
```console
docker-compose up -d
```
- stop container
```console
docker-compose down
```

- airflow bash
- open bash of scheduler in interactive mode
```console
docker exec -it airflow-playground-airflow-scheduler-1 /bin/bash
docker exec -it airflow-playground-airflow-webserver-1 /bin/bash
```

- airflow commands
```console
airflow tasks test <DAG NAME> <TASK NAME> <SCHEDULER START DATE>
airflow tasks test user_processing create_table 2024-10-20
```