from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from flask import jsonify
from flask import render_template
import os, json
from bson.json_util import dumps
import requests

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/projet_velib"
client = PyMongo(app)

ref = client.db.stations_records.aggregate([
	{"$group": {"_id" :{"code_station": "$station.code",
				"nom_station": "$station.name"}}},
])
referentiel_stations = {}
for station in ref:
	for _id in station:
		tmp = []
		for key in station[_id]:
			tmp.append(station[_id][key])
		referentiel_stations[tmp[1]] = tmp[0]

# TODO:
# 1 PAR STATION : Volume( nombre velo dispo / emprumter) emprun retour temps réel + par rapport aux heures
# 2 Prédiction - Quelles stations ont le + de chance de pouvoir donner/recevoir un vélo

@app.route('/', methods=['GET', 'POST'])
def home():
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "static\\data", "nom_stations.json")
	json_data = json.load(open(json_url, encoding='utf-8'))
	
	return render_template("index.html", json_data=json.dumps(json_data, ensure_ascii=False).encode('utf-8'))

# Real-time API requesting for not-prediction data
@app.route('/stations', methods=['GET', 'POST'])
def get_one():
	'''# Retourne le code de la station passé dans la requête
	res = client.db.stations_records.find_one(
		{"station.name": request.args.get('name')},
		{"station.code": 1}
	)

	station_records = client.db.station_records.find(
		{"station.name": request.args.get('name')},
	)
	print("\n\n\n", dumps(station_records))
'''
	StartPoint = ["49","2.85"]
	EndPoint = ["48.7","2"]
	URL = "https://www.velib-metropole.fr/webapi/map/details?gpsTopLatitude="+StartPoint[0]+"&gpsTopLongitude="+StartPoint[1]+"&gpsBotLatitude="+EndPoint[0]+"&gpsBotLongitude="+EndPoint[1]+"&zoomLevel=19"

	resp = requests.get(URL)
	formatted_resp = resp.text
	print(type(formatted_resp))

	return formatted_resp

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')