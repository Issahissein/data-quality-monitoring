from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime


PROJECT_DIR = "/home/issah/data-quality-monitoring"


with DAG(
    dag_id="data_quality_monitoring",
    start_date=datetime(2026, 1, 1),
    schedule="@hourly",
    catchup=False,
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="python extract_data.py {{ ds }}",
        cwd=PROJECT_DIR,
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="python transform_data.py",
        cwd=PROJECT_DIR,
    )

    extract >> transform