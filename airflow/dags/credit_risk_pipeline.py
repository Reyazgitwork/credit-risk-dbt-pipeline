from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="credit_risk_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["dbt"]
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="echo running dbt run"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="echo running dbt test"
    )

    dbt_run >> dbt_test