from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from subprocess import call
import os
from pytz import timezone
from scrapyfbref.scrapyfbref.spiders.spider1_aws import MySpiderForPlayers
#from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

S3_BUCKET_NAME = 'fbrefdata0921'
S3_KEY = 'output/fbref.csv'

os.chdir('./dags/scrapyfbref/')
local_tz = timezone('Asia/Singapore')
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 21, tzinfo=local_tz),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('scrapy_fbref_players', default_args=default_args, schedule_interval=timedelta(days=1))

def run_spider():
  #  root_dir = os.path.abspath(os.path.join(os.sep, "var", "data", "webserver"))
    logger.info(f"The first root directory is {os.getcwd()}.")
    call(["scrapy", "crawl", "fbref","-s","CLOSESPIDER_PAGECOUNT=10"])
    logger.info(f"The second root directory is {os.getcwd()}.")
def upload_to_s3():
  #  root_dir = os.path.abspath(os.path.join(os.sep, "var", "data", "webserver"))
    logger.info(f"The root directory is {os.getcwd()}.")    
    # s3 = S3Hook()
    # s3.load_file(
    #     filename='./scrapyfbref/file.csv',
    #     key=S3_KEY,
    #     bucket_name=S3_BUCKET_NAME,
    #     replace=True
    # )


scrapy_task = PythonOperator(task_id='run_spider', python_callable=run_spider, dag=dag)
load_file = PythonOperator(task_id='upload_to_s3', python_callable=upload_to_s3, dag=dag)

scrapy_task >> load_file