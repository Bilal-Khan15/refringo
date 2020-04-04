import requests 
import xml.etree.ElementTree as ET 
import pymongo
from flask import Flask, request, jsonify, make_response, session, flash, get_flashed_messages, render_template, redirect
from flask_session import Session
from flask_cors import CORS, cross_origin
from snippet import rich
import os
from flask import render_template
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import ui
from flask_api import status

app = Flask(__name__)
cors = CORS(app)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["refringo"]
SCOPES = [ "https://www.googleapis.com/auth/indexing" ]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
JSON_KEY_FILE = "api-266117-e97bc7b404ed.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
http = credentials.authorize(httplib2.Http())
prev = ""


def loadXML(url): 
	resp = requests.get(url) 

	with open('jobfeed.xml', 'wb') as f: 
		f.write(resp.content) 
		

def parseXML(file): 
   with open('templates/'+file, "a", encoding='utf-8') as site:
      site.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+'\n')
      tree = ET.parse('jobfeed.xml')
      root = tree.getroot()

      for elem in root:
         job = {}
         
         for subelem in elem:
            
            job[str(subelem.tag)] = str(subelem.text)

         try:
            site.write('<url>'+'\n'+'<loc>http://refringo.com:8080/templates/'+str(job['job-code'])+'.html</loc>'+'\n'+'</url>'+'\n')
            content = {
               "url": "http://refringo.com:8080/templates/"+str(job['job-code'])+".html",
               "type": "URL_UPDATED"
            }

         except:
            site.write('<url>'+'\n'+'<loc>http://refringo.com:8080/templates/'+str(job['jobid'])+'.html</loc>'+'\n'+'</url>'+'\n')
            content = {
               "url": "http://refringo.com:8080/templates/"+str(job['jobid'])+".html",
               "type": "URL_UPDATED"
            }

         job['description'] = job['description'].replace('"', '\\"').replace("'","\\'")
         rich(job)
         result = mydb.jobs.insert_one(job)
         # response, content = http.request(ENDPOINT, method="POST", body=str(content))
         # if(response['status'] != '200'):
         #    print(response)

      site.write('</urlset>')


@cross_origin
@app.route('/job', methods=['GET'])
def job(url=""):
   url = request.args.get('url')
   cur = mydb.jobs.find_one({"url": url}, { "_id": 0})

   return jsonify({'jobs': cur})


@cross_origin
@app.route('/templates/<id>', methods=['GET'])
def index(id):
   return render_template(str(id))


@cross_origin
@app.route('/jobs', methods=['GET'])
def search(country="", city="", title=""):
   country = request.args.get('country')
   city = request.args.get('city')
   title = request.args.get('title')

   # query = dict(request.form)
   # country = query['country'][0]
   # city = query['city'][0]
   # title = query['title'][0]

   jobs = []
   q = {}
   if(country):
      q["country"] = country
   if(city):
      q["city"] = city
   if(title):
      q["title"] = title

   cur = mydb.jobs.find(q,{ "_id": 0}).limit(100)
   for doc in cur:
      jobs.append(doc)

   return jsonify({'jobs': jobs})


@cross_origin
@app.route('/city', methods=['GET'])
def city(country=""):
   country = request.args.get('country')

   city = mydb.jobs.find({ "country": country}).distinct('city')

   return jsonify({'city': city})


def page_is_loaded(driver):
    return driver.current_url != prev

@cross_origin
@app.route('/apply', methods=['GET'])
def apply(url=""):
   url = request.args.get('url')
   options = Options()
   options.headless = True
   driver = webdriver.Firefox(options=options)
   driver.get(url)
   try:
      xpath = '//*[@id="apply-action"]'
      btn = driver.find_element_by_xpath(xpath)
      btn.click()
      xpath = '//*[@id="user-email-alert"]'
      box = driver.find_element_by_xpath(xpath)
      box.send_keys('friediruegen84@gmail.com')
      box.submit()
      prev = driver.current_url
      wait = ui.WebDriverWait(driver,10)
      wait.until(page_is_loaded)
      driver.save_screenshot('screen.png')
      newURL = driver.current_url
   except:
      newURL = url
   return jsonify({'newURL': newURL})


@cross_origin
@app.route('/addPage', methods=['POST'])
def addPage():
   page = dict(request.form)
   description = page['description']
   typeof = page['typeof']

   page_request = {
      'description': description,
      'typeof': typeof
   }
   mydb.page.insert_one(page_request)

   return jsonify({'response': 'Page Added'})


@cross_origin
@app.route('/deletePage', methods=['GET'])
def deletePage():
   typeof = request.args.get('typeof')

   mydb.page.remove({'typeof': typeof})

   return jsonify({'response': 'Page Deleted'})


@cross_origin
@app.route('/readPage', methods=['GET'])
def readPage():
   typeof = request.args.get('typeof')

   page = mydb.page.find_one({'typeof': typeof}, { "_id": 0})
   if(page == None):
      return jsonify({'response': 'Not available! '}), status.HTTP_404_NOT_FOUND
   else:
      return jsonify({'response': page})


@cross_origin
@app.route('/lists', methods=['GET'])
def lists():
   title = mydb.jobs.distinct('title')
   country = mydb.jobs.distinct('country')
   city = mydb.jobs.distinct('city')

   return jsonify({'title': title, 'country':country, 'city': city})


@cross_origin
@app.route('/drop', methods=['GET'])
def drop():
   mydb.jobs.drop()

   open('templates/sitemap_index.xml', 'w').close()

   mydir = './templates/'

   filelist = [ f for f in os.listdir(mydir) if f.endswith(".xml") ]
   for f in filelist:
      os.remove(os.path.join(mydir, f))

   filelist = [ f for f in os.listdir(mydir) if f.endswith(".html") ]
   for f in filelist:
      os.remove(os.path.join(mydir, f))

   return jsonify({'response': "cleared!"})


@cross_origin
@app.route('/test', methods=['GET'])
def main(): 
   x = 0
   with open('templates/'+"sitemap_index.xml", "a", encoding='utf-8') as myfile:
      myfile.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n'+'<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+'\n')
      with open('feedLinks.txt','r') as f:
         for line in f:
            link = line.split("&page=1&of=1")
            # for i in range(1,101):
            for i in range(1,2):
               URL = link[0] + "&page=" + str(i) + "&of=100"
               print("Now fetching data from '" + URL + "' ...")
               loadXML(URL) 
               print("Fetching completed ..")
               myfile.write('<sitemap>'+'\n'+'<loc>http://refringo.com:8080/templates/sitemap_'+str(x)+'.xml</loc>'+'\n'+'</sitemap>'+'\n')
               jobitems = parseXML('sitemap_'+str(x)+'.xml') 
               x = x + 1
               print("Saving to DB completed .")
      myfile.write('</sitemapindex>')

   requests.get("http://www.google.com/ping?sitemap=http://refringo.com:8080/templates/sitemap_index.xml")

   return jsonify({'response': "Job feeds updated!"})


if __name__ == '__main__':
    app.run(host="0.0.0.0",port='8080',debug=True)







# http://www.google.com/ping?sitemap=http://refringo.com:8080/templates/sitemap_index.xml








# keyword, profession, country, city, zip code, company

# import zipcodes
# print(zipcodes.matching('57128'))
# # https://pypi.org/project/zipcodes/

# import pgeocode
# nomi = pgeocode.Nominatim('fr')
# print(nomi.query_postal_code("75260"))
# # https://github.com/symerio/pgeocode

# import re
# pat = re.compile(r'us|IT', re.I)
# cur = mydb.jobs.find({ "country": {'$regex': pat}})
# for doc in cur:
#    print(doc)

# cur = mydb.jobs.distinct('title')
# print(cur)


# cur = mydb.jobs.find({ "country": "US"}).distinct('city')
# for doc in cur:
#    print(doc)



# print(len(cur))





# ENDPOINT = "http://refringo.com:8080/lists"

# response = http.request(ENDPOINT, method="GET")

# print(response)








# today = 1585699200.0000
# now = datetime.now()
# timestamp = datetime.timestamp(now)
# if(timestamp >= today+86400):
#    today = today+86400
#    print('Bilal')
