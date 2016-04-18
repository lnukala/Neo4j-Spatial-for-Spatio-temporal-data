from flask import Flask, request
from flask_restful import  Resource, Api
import requests
import json

app = Flask(__name__)
api = Api(app)

#Run the within distance query and return the values in that circle
class WithinDistance (Resource):
    def get(self):
        data = json.loads(request.get_data())
        url = 'http://localhost:7474/db/data/ext/SpatialPlugin/graphdb/findGeometriesWithinDistance'
        payload = {"layer" : data.get('date'),  'pointX': data.get('lon'), 'pointY': data.get('lat'),
                   "distanceInKm" : data.get('distance')}
        print(payload)
        r = requests.post(url, data=json.dumps(payload), auth=('neo4j', '18843'))
        if r.status_code != 200:
            return "Error!", r.status_code
        content = json.loads(r.content)
        data = []
        for object in content :
            if 'value' in object['data']:
                info = {
                    'value' : object['data'].get('value'),
                    'lat' : object['data'].get('lat'),
                    'lon' : object['data'].get('lon')
                }
                data.append(info)
        return json.dumps(data)

#For bounding box queries
class BBox (Resource):
    def get(self):
        data = json.loads(request.get_data())
        url = 'http://localhost:7474/db/data/ext/SpatialPlugin/graphdb/findGeometriesInBBox'
        payload = {"layer" : data.get('date'),  'miny':data.get('miny'), 'maxy': data.get('maxy'),
                  'minx': data.get('minx'), 'maxx':data.get('maxx')}
        r = requests.post(url, data=json.dumps(payload), auth=('neo4j', '18843'))
        if r.status_code != 200:
            return "Error!", r.status_code
        content = json.loads(r.content)
        data = []
        for object in content :
            if 'value' in object['data']:
                info = {
                    'value' : object['data'].get('value'),
                    'lat' : object['data'].get('lat'),
                    'lon' : object['data'].get('lon')
                }
                data.append(info)
        return json.dumps(data)

api.add_resource(WithinDistance, '/withindist/')
api.add_resource(BBox, '/boundingbox')

if __name__ == '__main__':
    app.run()