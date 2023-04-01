from datetime import datetime
import json
import mysql.connector
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'kartaca',
    'start_date': datetime(2023, 4, 1, 10, 5, 0),
}

dag = DAG(
    'currency',
    default_args=default_args,
    schedule_interval='0 10 * * *',
)

def start_dag():
    print("DAG started.")

def read_json():
    with open('data\country_currency.json', 'r') as f:
        data = json.load(f)
    return data

def insert_data():
    data = read_json()
    conn = mysql.connector.connect(host='db', user='kartaca', password='kartaca', database='kartaca')
    cursor = conn.cursor()
    for row in data:
        sql = "INSERT INTO currency (id, code, name) VALUES (%s, %s, %s)"
        val = (row['id'], row['code'], row['name'])
        cursor.execute(sql, val)
    conn.commit()
    cursor.close()
    conn.close()

def end_dag():
    print("DAG completed.")

start_task = PythonOperator(
    task_id='start',
    python_callable=start_dag,
    dag=dag,
)

read_json_task = PythonOperator(
    task_id='read_json',
    python_callable=read_json,
    dag=dag,
)

insert_data_task = PythonOperator(
    task_id='insert_data',
    python_callable=insert_data,
    dag=dag,
)

end_task = PythonOperator(
    task_id='end',
    python_callable=end_dag,
    dag=dag,
)

start_task >> read_json_task >> insert_data_task >> end_task
