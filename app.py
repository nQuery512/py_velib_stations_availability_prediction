import io, subprocess
import requests
import time
from pymongo import MongoClient


#### SETTINGS PART ####
# Coordinates URL parameter 
StartPoint = ["49","2.85"]
EndPoint = ["48.7","2"]
URL = "https://www.velib-metropole.fr/webapi/map/details?gpsTopLatitude="+StartPoint[0]+"&gpsTopLongitude="+StartPoint[1]+"&gpsBotLatitude="+EndPoint[0]+"&gpsBotLongitude="+EndPoint[1]+"&zoomLevel=19"
# Set file settings
timestamp = str(time.strftime("%d_%m_%Y-%Hh-%M-%S"))
filename = "donnee_stations_paris_" + timestamp +".json"

# Output json file creation
output_file = io.open("json/"+filename, "a+", encoding="utf8")

#### DATA ACQUISITION ###
# GET Request 
resp = requests.get(URL)
# Response encoding for special symbols
resp.encoding = "utf-8"
# Writing json request response into output file 
output_file.write(str(resp.content.decode("utf-8")))
print(filename)

#### STORE AND TIMESTAMPING RECORDS ####
# Set up connection to database
client = MongoClient('localhost', 27017)
# Get the good database/collection
collection = client['velib_stations']['stations_records']
# Run file import into mongodb by subprocess (shell)
subprocess.run(["mongoimport", "--jsonArray", "--db", "velib_stations"
	, "--collection", "stations_records", "--file", "json/"+filename])
# Timestamping all station_records
collection.update_many({'time_stamp': {'$exists': False}},
                        {'$set' : {'time_stamp':timestamp}},
                        upsert = False) 

#### CLEANING UP AND EXITING ####
# Closing database connection
client.close()