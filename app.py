from flask import Flask, render_template, request, redirect, url_for
import os
from subprocess import call



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
            os.chdir('dags/scrapyfbref/')
        except:
            pass
        a = os.getcwd()
        call(["scrapy", "crawl", "fbref","-s","CLOSESPIDER_PAGECOUNT=3"])
        os.chdir('.')        
        return (f"success")


########################main page
if __name__ == "__main__":    
    app.run(port=8000, debug=True, threaded=True)
