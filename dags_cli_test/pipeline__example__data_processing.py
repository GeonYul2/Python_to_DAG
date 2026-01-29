"""
Generated DAG: pipeline__example__data_processing
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
from datetime import datetime, timedelta

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
    schedule_interval="@daily",
    catchup=False,
    tags=["example", "data"],
) as dag:

    # Task Definitions

    extract_data = PythonOperator(
        task_id="extract_data",
        python_callable=lambda: print(
            "Executing extract"
        ),  # Placeholder for actual callable import
        op_kwargs={"source": "api"},
    )

    transform_data = PythonOperator(
        task_id="transform_data",
        python_callable=lambda: print(
            "Executing transform"
        ),  # Placeholder for actual callable import
        op_kwargs={},
    )

    load_data = PythonOperator(
        task_id="load_data",
        python_callable=lambda: print(
            "Executing load"
        ),  # Placeholder for actual callable import
        op_kwargs={},
    )

    # Dependencies

    extract_data >> transform_data

    transform_data >> load_data
