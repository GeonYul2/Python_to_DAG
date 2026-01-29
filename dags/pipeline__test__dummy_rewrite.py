"""
Generated DAG: pipeline__test__dummy_rewrite
"""
from airflow import DAG
import pendulum
from datetime import datetime, timedelta

# Operator Imports

from airflow.operators.empty import EmptyOperator

from airflow.operators.python import PythonOperator


# Default arguments
default_args = {
    "owner": "test",
    "retries": 1,
    "retry_delay": timedelta(seconds=300),
}

# Pipeline Definition
with DAG(
    dag_id="pipeline__test__dummy_rewrite",
    default_args=default_args,
    schedule_interval="@once",
    catchup=False,
    tags=[],
) as dag:

    # Task Definitions

    legacy_dummy = EmptyOperator(
        task_id="legacy_dummy",
    )

    legacy_python = PythonOperator(
        task_id="legacy_python",
        python_callable=lambda: print("Executing None"),  # Placeholder
    )

    # Dependencies

    legacy_dummy >> legacy_python
