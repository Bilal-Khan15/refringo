import requests 
import xml.etree.ElementTree as ET 
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["refringo"]


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

      result = mydb.jobs.insert_one(job)


def search(country="", city="", title=""):
   q = {}
   if(country):
      q["country"] = country
   if(city):
      q["city"] = city
   if(title):
      q["title"] = title

   cur = mydb.jobs.find(q,{ "_id": 0, "title": 1, "country": 1 })
   for doc in cur:
      print(doc)


def main(): 

#    with open('feedLinks.txt','r') as f:
#       for line in f:
#          link = line.split("&page=1&of=1")
#          # for i in range(1,101):
#          for i in range(1,2):
#             URL = link[0] + "&page=" + str(i) + "&of=100"
#             print("Now fetching data from '" + URL + "' ...")
#             loadXML(URL) 
#             print("Fetching completed ..")
#             jobitems = parseXML() 
#             print("Saving to DB completed .")

#    # mydb.jobs.drop()

   # search("IT", "", "")
	
if __name__ == "__main__": 
	main() 
















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
