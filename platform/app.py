from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from flask import jsonify
from flask import render_template
import os, json
from bson.json_util import dumps
import requests

import classifier

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

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/rt-search', methods=['GET', 'POST'])
def real_time_search():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static\\data", "nom_stations.json")
    json_data = json.load(open(json_url, encoding='utf-8'))
    return render_template('realtime-search.html', json_data=json.dumps(json_data, ensure_ascii=False).encode('utf-8'))

@app.route('/predict-search', methods=['GET', 'POST'])
def geographic_prediction_search():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static\\data", "nom_stations.json")
    json_data = json.load(open(json_url, encoding='utf-8'))
    return render_template('predict-search.html', json_data=json.dumps(json_data, ensure_ascii=False).encode('utf-8'))

# Real-time API requesting for not-prediction data
@app.route('/stations', methods=['GET', 'POST'])
def get_one():
    StartPoint = ["49","2.85"]
    EndPoint = ["48.7","2"]
    URL = "https://www.velib-metropole.fr/webapi/map/details?gpsTopLatitude="+StartPoint[0]+"&gpsTopLongitude="+StartPoint[1]+"&gpsBotLatitude="+EndPoint[0]+"&gpsBotLongitude="+EndPoint[1]+"&zoomLevel=19"

    resp = requests.get(URL)
    formatted_resp = resp.text
    print(type(formatted_resp))

    return formatted_resp

@app.route('/predict_stations', methods=['GET', 'POST'])
def get_nearest_station():
    hour = request.args.get('hour')
    filename_txt = str('data_h\\'+hour+'.txt')
    filename = str('data_h\\'+hour+'.pkl')
    
    testFeatures = classifier.get_test_features(filename_txt)

    model = classifier.get_model(filename)

    # Appel de la fonction de prediction
    result = classifier.predict(model, testFeatures)
    print(result)
    # TODO: - Récupération des données de la carte open street map 
    #       - Utilisation de requête geospatial + utilisation $geoNear geospatial request operator
    #       - Test comparatif à l'aide des données temps réels
    return str(result)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')