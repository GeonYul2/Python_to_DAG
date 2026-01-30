"""
Generated DAG: pipeline__example__data_processing
"""
from airflow import DAG
import pendulum
from datetime import datetime, timedelta

# Operator Imports

from airflow.providers.standard.operators.python import PythonOperator


# Default arguments
default_args = {
    "owner": "data_team",
    "retries": 3,
    "retry_delay": timedelta(seconds=600),
    "start_date": pendulum.parse("2023-01-01"),
}

# Pipeline Definition
with DAG(
    dag_id="pipeline__example__data_processing",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    tags=["example", "data"],
) as dag:

    # Task Definitions

    # 1. Root Tasks (No Group)

    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=lambda: print("Executing extract"),
        op_kwargs={"source": "api"},
    )

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=lambda: print("Executing transform"),
    )

    load_data = PythonOperator(
        task_id="load_data",
        python_callable=lambda: print("Executing load"),
    )

    # 2. Task Groups

    # Dependencies

    extract_data >> transform_data

    transform_data >> load_data
