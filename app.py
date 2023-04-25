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

######################Set up variables for use in our script
app = Flask(__name__)


def method():
    whereami = os.path.abspath(os.getcwd())
    try:
        os.chdir('dags/scrapyfbref/')
    except:
        pass
    print("1",os.getcwd())
    os.system('scrapy crawl fbref -s JOBDIR=crawls/somespider-1 -o output1.csv:csv')
    client = boto3.client("s3", aws_access_key_id=None,
         aws_secret_access_key= None)
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    client.upload_file("output1.csv", "fbrefdata0922", f"output/output_{time}.csv")
    os.chdir(whereami)   


########################main page
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        print('Scheduler initialised')
        schedule.every(10).minutes.do(method)
        print('Next job is set to run at: ' + str(schedule.next_run()))
        while True:
            schedule.run_pending()
            time.sleep(1)

    return

@app.route('/scrape', methods = ['GET', 'POST'])
def scrape():
    if request.method == 'GET':
        whereami = os.path.abspath(os.getcwd())
        try :
            os.chdir('dags/scrapyfbref/')
            print("1",os.getcwd())
        except:
            print("2",os.getcwd())
     #   call(["scrapy", "crawl", "fbref","-s","CLOSESPIDER_PAGECOUNT=30","-o","output.csv"])
    #    call(["scrapy", "crawl", "fbref","-s","CLOSESPIDER_PAGECOUNT=8","-o","output1.csv"])
        call(["scrapy", "crawl", "fbref","-o","output1.csv", "-t","csv"])
        os.chdir(whereami)        
        return (f"success")
    
@app.route("/download", methods = ["GET", "POST"])
def download():
    if request.method == 'GET':
        whereami = os.path.abspath(os.getcwd())
        try:
            os.chdir('dags/scrapyfbref/')
        except:
            pass
        #os.chdir('dags/scrapyfbref/')
        temp1 = os.path.abspath(os.getcwd())
        os.chdir(os.path.abspath(os.getcwd()))            
        temp2 = os.path.abspath(os.getcwd())
        os.chdir(whereami)
        try :
            return send_from_directory(directory=temp1, path="output1.csv")
        except Exception as e:
            return (f"Error {temp1}, {temp2}, {e}")
  
    return (f"Run The Scraper")

########################main page
if __name__ == "__main__":    
    app.run(port=8000, debug=True)