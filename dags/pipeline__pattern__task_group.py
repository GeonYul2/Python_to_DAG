"""
Generated DAG: pipeline__pattern__task_group
"""
from airflow import DAG
import pendulum
from datetime import datetime, timedelta

# Operator Imports

from airflow.operators.empty import EmptyOperator

from airflow.utils.task_group import TaskGroup


# Default arguments
default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(seconds=300),
}

# Pipeline Definition
with DAG(
    dag_id="pipeline__pattern__task_group",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    tags=[],
) as dag:

    # Task Definitions

    # 1. Root Tasks (No Group)

    start = EmptyOperator(
        task_id="start",
    )

    end = EmptyOperator(
        task_id="end",
    )

    # 2. Task Groups

    with TaskGroup(
        group_id="ingest_group", tooltip="Task Group: ingest_group"
    ) as ingest_group:

        extract = EmptyOperator(
            task_id="extract",
        )

        load = EmptyOperator(
            task_id="load",
        )

    # Dependencies

    start >> extract

    extract >> load

    load >> end
