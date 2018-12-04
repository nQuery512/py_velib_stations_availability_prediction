from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from pymongo import GEO2D
from flask import jsonify
from flask import render_template
import os, json

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
    # Récupération des arguments de l'URL
    hour = request.args.get('hour')
    gps_lat = request.args.get('lat')
    gps_long = request.args.get('long')
    perimeter = request.args.get('perimeter')

    print('\n\n\n',perimeter,'\n\n\n')

    # Création dynamique des noms de fichiers pour ouverture uniquement
    filename_txt = str('data_h\\'+hour+'.txt')
    filename = str('data_h\\'+hour+'.pkl')
    
    '''
    # Création des features et modèles
    #trainingFeatures = classifier.get_training_features(filename_txt)
    #model = classifier.get_model(filename)

    # Appel de la fonction de prediction
   
    #result = classifier.predict(model, trainingFeatures)
    print(len(result))
    print(type(result))
    
    for record in result:
        print(result[record])
    '''

    # Filtrage via la base mongodb
    result =classifier.classify(8)
    test_dist = 0

    client.db.stations_records.create_index([("station.location.coordinates", "2dsphere")])
    near_station = client.db.stations_records.aggregate([
    {   
        "$geoNear": 
        {   
            "near": 
            {
                "type": "Point", "coordinates": [float(gps_lat), float(gps_long)]
            },
            "distanceField": "station.location.calculated",
            "maxDistance": int(perimeter),
            "num":1000000,
            "spherical": True    
        }
    },
    {"$unwind":"$station.location.coordinates"},
    {
        "$group": 
        {
            "_id": "$_id",
            "station_name":
            { 
                "$first": "$station.name"
            },
            "station_gps":
            {
                "$push": "$station.location.coordinates"
            },
            "station_distance": 
            {
                "$first": "$station.location.calculated"
            }
        }
    }
    ])
    clean_station = []
    clean_station_name = []
    for station in near_station:
        if(station['station_name'] not in clean_station_name):
            del station['_id']
            clean_station.append(station)
            clean_station_name.append(station['station_name'])
    #print(clean_station)

    is_near_count = 0
    new_list = []
    for i, near_station_name in enumerate(clean_station_name):
        is_near = False
        for record in result:
            #print(near_station_name, record)
            if near_station_name in record:
                #print('IDENTIQUE ', near_station_name, result[record])
                is_near = True
                is_near_count +=1
                break
        if(is_near == True):
            new_list.append(clean_station[i])
            new_list[is_near_count-1]['station_proba']=result[record]

    total = 0
    # Recalcul du pourcentage

    for station in new_list:
        total += station['station_proba']
    for station in new_list:
        station['station_proba'] = int((station['station_proba'] * 100)/total)

    print(new_list)
    return str(new_list[::-1])

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')