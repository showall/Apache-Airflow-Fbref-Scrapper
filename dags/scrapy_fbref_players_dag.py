from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from subprocess import call
import os
from airflow.utils.dates import timezone
from scrapyfbref.scrapyfbref.spiders.spider1 import MySpiderForPlayers

os.chdir('/home/gerardsho/airflow/dags/scrapyfbref/')
local_tz = timezone.get_localzone()
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 21, tzinfo=local_tz),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('scrapy_fbref_players', default_args=default_args, schedule_interval=timedelta(days=1))

def run_spider():
    call(["scrapy", "crawl", "fbref"])

scrapy_task = PythonOperator(task_id='run_spider', python_callable=run_spider, dag=dag)


