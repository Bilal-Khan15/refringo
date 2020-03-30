import requests 
import xml.etree.ElementTree as ET 
import pymongo
from flask import Flask, request, jsonify, make_response, session, flash, get_flashed_messages, render_template, redirect
from flask_session import Session
from flask_cors import CORS, cross_origin
from snippet import rich

app = Flask(__name__)
cors = CORS(app)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["refringo"]

from flask import render_template


def loadXML(url): 
	resp = requests.get(url) 

	with open('jobfeed.xml', 'wb') as f: 
		f.write(resp.content) 
		

def parseXML(): 
   tree = ET.parse('jobfeed.xml')
   root = tree.getroot()

   for elem in root:
      job = {}
      
      for subelem in elem:
         
         job[str(subelem.tag)] = str(subelem.text)

      rich(job)
      result = mydb.jobs.insert_one(job)


@cross_origin
@app.route('/jobs/<id>', methods=['GET'])
def index(id):
   return render_template(str(id)+".html")


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
@app.route('/drop', methods=['GET'])
def drop():
   mydb.jobs.drop()
   return jsonify({'response': "DB cleared!"})


@cross_origin
@app.route('/test', methods=['POST'])
def main(): 
   with open('feedLinks.txt','r') as f:
      for line in f:
         link = line.split("&page=1&of=1")
         # for i in range(1,101):
         for i in range(1,2):
            URL = link[0] + "&page=" + str(i) + "&of=100"
            print("Now fetching data from '" + URL + "' ...")
            loadXML(URL) 
            print("Fetching completed ..")
            jobitems = parseXML() 
            print("Saving to DB completed .")

   # search("IT", "", "")

   return jsonify({'response': "Job feeds updated!"})
	
if __name__ == '__main__':
    app.run(host="0.0.0.0",port='80',debug=True)
















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

# cur = mydb.jobs.distinct('country')
# print(cur)


# cur = mydb.jobs.find({ "country": "US"}).distinct('city')
# for doc in cur:
#    print(doc)
