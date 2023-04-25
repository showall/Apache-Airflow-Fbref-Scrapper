from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from subprocess import call
from datetime import datetime, timedelta
from pytz import timezone
from dags.scrapyfbref.scrapyfbref.spiders.spider1_aws import MySpiderForPlayers
import logging


######################Set up variables for use in our script
app = Flask(__name__)

########################main page
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return ("Welcome, Please go to /scrape")
    
@app.route('/scrape', methods = ['GET', 'POST'])
def scrape():
    if request.method == 'GET':
        try :
            os.chdir('dags/scrapyfbref')
        except:
            pass
        a = os.getcwd()
     #   call(["scrapy", "crawl", "fbref","-s","CLOSESPIDER_PAGECOUNT=30","-o","output.csv"])
        call(["scrapy", "crawl", "fbref","-s","CLOSESPIDER_PAGECOUNT=8","-o","output1.csv"])
        #os.chdir('.')        
        return (f"success")
    
@app.route("/download", methods = ["GET", "POST"])
def download():
    if request.method == 'GET':
        try:           
            os.chdir('dags/scrapyfbref')
            #os.chdir('dags/scrapyfbref/')
            temp1 = os.path.abspath(os.getcwd())
            os.chdir('')            
            temp2 = os.path.abspath(os.getcwd())
            return send_from_directory(directory=temp1, path="output1.csv")
        except Exception as e:
            return (f"Error {temp1}, {temp2}, {e}")
    return (f"Run The Scraper")

########################main page
if __name__ == "__main__":    
    app.run(port=8000, debug=True)
