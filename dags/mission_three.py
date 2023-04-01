from datetime import datetime, timedelta
import json
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 4, 2, 10, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'data_merge',
    default_args=default_args,
    schedule_interval=timedelta(days=1)
)


def start_log():
    print("DataMerge-DAG started")


def merge_data():
    mysql_hook = MySqlHook(mysql_conn_id='mysql_conn')# MySQL connection

    
    clear_table_query = "TRUNCATE TABLE data_merge"# Clear the data_merge table
    mysql_hook.run(clear_table_query)

    # Merge the country and currency tables and insert into data_merge table
    merge_query = """
        INSERT INTO data_merge (country_code, country_name, currency_code, currency_name)
        SELECT country.country_code, country.country_name, currency.currency_code, currency.currency_name
        FROM country
        INNER JOIN currency ON country.currency_code = currency.currency_code
    """
    mysql_hook.run(merge_query)

def end_log():
    print("Data Merge DAG finished")


start_task = PythonOperator(
    task_id='start_log',
    python_callable=start_log,
    dag=dag
)

merge_task = PythonOperator(
    task_id='merge_data',
    python_callable=merge_data,
    dag=dag
)

end_task = PythonOperator(
    task_id='end_log',
    python_callable=end_log,
    dag=dag
)

start_task >> merge_task >> end_task
