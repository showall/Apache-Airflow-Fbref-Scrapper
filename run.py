from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from subprocess import call
from datetime import datetime, timedelta
from pytz import timezone
from dags.scrapyfbref.scrapyfbref.spiders.spider1_aws import MySpiderForPlayers
import logging
import schedule
import os
import time
import boto3
import requests

######################Set up variables for use in our script

bucket_name = "fbrefdata0922"

def run():
    def method():
        whereami = os.path.abspath(os.getcwd())
        try:

            os.chdir('dags/scrapyfbref/')
            logging.basicConfig(level=logging.DEBUG)
            INFO1 = os.getcwd()
            logging.info(f"Changed to {INFO1}")
            logging.basicConfig(level=logging.WARN)
            os.system('scrapy crawl fbref -s JOBDIR=crawls/somespider-1 -o output1.csv')
            client = boto3.client("s3", aws_access_key_id="AKIASCUU2GL3UMLBKS4M",
                aws_secret_access_key= "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")
            time = datetime.now().strftime("%Y%m%d%H%M%S")
            logging.basicConfig(level=logging.DEBUG)
        # logging.info(f"2 {os.getcwd()}")
            logging.basicConfig(level=logging.WARN)
            try:
                client.upload_file("output1.csv", "fbrefdata0922", f"output/outputrun_{time}.csv")
            except:
                try:
                    with open("output1.csv", 'rb') as f:
                        response = requests.put(f'https://{bucket_name}.s3.amazonaws.com/output/output2_{time}.csv', data=f)
                except:
                    pass
            os.chdir(whereami) 
        except:
            logging.basicConfig(level=logging.DEBUG)
            logging.info(f"Not Managed to Change {os.getcwd()}")
            logging.basicConfig(level=logging.WARN)
        return

    def log_next_run(tag):
        logging.info('Next job is set to run at: ' + str(schedule.next_run(tag)))

    def method1():
        logging.basicConfig(level=logging.DEBUG)
        INFO1 = os.getcwd()
        logging.info(f"Changed to {INFO1}")

        logging.basicConfig(level=logging.WARN)
        return

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Hello...")
    logging.basicConfig(level=logging.WARN)
    logging.info('Scheduler initialised')
    logging.basicConfig(level=logging.DEBUG)
    
    schedule.every(5).minutes.do(method).tag("job1")
    schedule.every(5).minutes.do(lambda : log_next_run("job1"))


    while True:
        schedule.run_pending()
        time.sleep(60)


########################main page

if __name__ == "__main__":    

    run()