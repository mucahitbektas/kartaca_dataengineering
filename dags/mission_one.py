from datetime import datetime
import json
import mysql.connector
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'kartaca',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 1, 10),
    'retries': 1
}

dag = DAG('country',
          default_args=default_args,
          schedule_interval='0 10 * * *')

def log_start():
    print('DAG started at {}'.format(datetime.now()))

def read_json():
    with open('data\country_name.json') as json_file:
        data = json.load(json_file)
    return data

def write_to_mysql():
    cnx = mysql.connector.connect(user='kartaca', password='kartaca',
                                  host='db',
                                  database='kartaca')
    cursor = cnx.cursor()
    
    data = read_json()
    for item in data:
        query = "INSERT INTO country (id, name, continent) VALUES (%s, %s, %s)"
        values = (item['id'], item['name'], item['continent'])
        cursor.execute(query, values)
        cnx.commit()
    
    cursor.close()
    cnx.close()
    print('Data has been written to MySQL')

def log_end():
    print('DAG finished at {}'.format(datetime.now()))

start_task = PythonOperator(task_id='log_start',
                            python_callable=log_start,
                            dag=dag)

read_json_task = PythonOperator(task_id='read_json',
                                python_callable=read_json,
                                dag=dag)

write_to_mysql_task = PythonOperator(task_id='write_to_mysql',
                                     python_callable=write_to_mysql,
                                     dag=dag)

end_task = PythonOperator(task_id='log_end',
                          python_callable=log_end,
                          dag=dag)

start_task >> read_json_task >> write_to_mysql_task >> end_task
