from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from flask import jsonify
from flask import render_template
import os, json

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
# 1 Volume( nombre velo dispo / emprumter) emprun retour temps réel + par rapport aux heures
# 2 Prédiction - Quelles stations ont le + de chance de pouvoir donner/recevoir un vélo

@app.route('/', methods=['GET', 'POST'])
def home():
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "static\\data", "nom_stations.json")
	json_data = json.load(open(json_url, encoding='utf-8'))
	
	return render_template("index.html", json_data=json.dumps(json_data, ensure_ascii=False).encode('utf-8'))

# http://localhost:5000/stations?station_id=16104
@app.route('/stations', methods=['GET', 'POST'])
def get_one():
	station_id = request.args.get('station_id')
	print("\n\n\n\n station_id:", station_id)
	count = client.db.stations_records.find({"station.code": station_id}).count()
	
	return str(count)

if __name__ == '__main__':

	app.run(debug=True,host='0.0.0.0')
