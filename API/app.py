from flask import Flask, request
from flask_restful import  Resource, Api
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)
api = Api(app)

#Run the within distance query and return the values in that circle
class WithinDistance (Resource):
    def post(self):
        data = json.loads(request.get_data())
        url = 'http://localhost:7474/db/data/ext/SpatialPlugin/graphdb/findGeometriesWithinDistance'
        payload = {"layer" : data.get('date'),  'pointX': data.get('lon'), 'pointY': data.get('lat'),
                   "distanceInKm" : data.get('distance')}
        r = requests.post(url, data=json.dumps(payload), auth=('neo4j', '18843'))
        if r.status_code != 200:
            return "Error!", r.status_code
        content = json.loads(r.content)
        data = []
        for object in content :
            if 'value' in object['data']:
                info = {
                    'co' : object['data'].get('co'),
                    'co2': object['data'].get('co2'),
                    'o3': object['data'].get('o3'),
                    'lat' : object['data'].get('lat'),
                    'lon' : object['data'].get('lon')
                }
                data.append(info)
        return json.dumps(data)

class Tile:
    def post(self):
        data = json.loads(request.get_data())
        url = 'http://localhost:7474/db/data/ext/SpatialPlugin/graphdb/findGeometriesWithinDistance'
        payload = {"layer": data.get('date'), 'pointX': data.get('lon'), 'pointY': data.get('lat'),
                   "distanceInKm": 0.28}
        r = requests.post(url, data=json.dumps(payload), auth=('neo4j', '18843'))
        if r.status_code != 200:
            return "Error!", r.status_code
        content = json.loads(r.content)
        data = []
        for object in content:
            if 'value' in object['data']:
                info = {
                    'co': object['data'].get('co'),
                    'co2': object['data'].get('co2'),
                    'o3': object['data'].get('o3'),
                    'lat': object['data'].get('lat'),
                    'lon': object['data'].get('lon')
                }
                data.append(info)
        return json.dumps(data)

#For bounding box queries
class BBox (Resource):
    def post(self):
        data = json.loads(request.get_data())
        url = 'http://localhost:7474/db/data/ext/SpatialPlugin/graphdb/findGeometriesInBBox'
        print data.get('date')
        print data.get('miny')
        payload = {"layer" : data.get('date'),  'miny':data.get('miny'), 'maxy': data.get('maxy'),
                  'minx': data.get('minx'), 'maxx':data.get('maxx')}
        r = requests.post(url, data=json.dumps(payload), auth=('neo4j', '18843'))
        if r.status_code != 200:
            return "Error!", r.status_code
        content = json.loads(r.content)
        data = []
        for object in content :
            if 'co' in object['data']:
                info = {
                    'co' : object['data'].get('co'),
                    'co2': object['data'].get('co2'),
                    'o3': object['data'].get('o3'),
                    'lat' : object['data'].get('lat'),
                    'lon' : object['data'].get('lon')
                }
                data.append(info)
        return json.dumps(data)

#get the tile data over a range of dates
class GetTile(Resource):
    def post(self):
        data = json.loads(request.get_data())
        date_format = "%Y-%m-%d"
        url = 'http://localhost:7474/db/data/ext/SpatialPlugin/graphdb/findGeometriesWithinDistance'
        date_list = [(datetime.strptime(data.get('end'), date_format) - timedelta(days=x)).strftime(date_format)
                     for x in range(0, (datetime.strptime(data.get('end'), date_format) - datetime.strptime(
                    data.get('start'), date_format)).days + 1)]
        result = []
        print date_list
        for date in reversed(date_list):
            payload = {"layer" : date,  'pointX': data.get('lng'), 'pointY': data.get('lat'),
                   "distanceInKm" : 0.28}
            r = requests.post(url, data=json.dumps(payload), auth=('neo4j', '18843'))
            if r.status_code != 200:
                print r.content
                return "Error!", r.status_code
            content = json.loads(r.content)
            values = []
            for object in content :
                if 'co' in object['data']:
                    info = {
                        'date' : date,
                        'co' : object['data'].get('co'),
                        'co2': object['data'].get('co2'),
                        'o3': object['data'].get('o3'),
                        'lat' : object['data'].get('lat'),
                        'lon' : object['data'].get('lon')
                    }
                    values.append(info)
            result.append(values)
        return json.dumps(result)

#Get the data for a box over a range of dates
class GetBox(Resource):
    def post(self):
        data = json.loads(request.get_data())
        date_format = "%Y-%m-%d"
        url = 'http://localhost:7474/db/data/ext/SpatialPlugin/graphdb/findGeometriesInBBox'
        date_list = [(datetime.strptime(data.get('end'), date_format) - timedelta(days=x)).strftime(date_format)
                     for x in range(0, (datetime.strptime(data.get('end'), date_format) - datetime.strptime(
                data.get('start'), date_format)).days + 1)]
        result = []
        print date_list
        for date in reversed(date_list):
            print date
            data.get('layer')
            print url
            payload = {'layer' : date , 'miny' : data.get('minlat'), 'maxy' : data.get('maxlat'),
                       'minx' : data.get('minlng'), 'maxx': data.get('maxlng')}
            r = requests.post(url, data=json.dumps(payload), auth=('neo4j', '18843'))
            if r.status_code != 200:
                print r.content
                return "Error!", r.status_code
            content = json.loads(r.content)
            values = []
            for object in content:
                if 'co' in object['data']:
                    info = {
                        'date': date,
                        'co': object['data'].get('co'),
                        'co2': object['data'].get('co2'),
                        'o3': object['data'].get('o3'),
                        'lat': object['data'].get('lat'),
                        'lon': object['data'].get('lon')
                    }
                    values.append(info)
            result.append(values)
        return json.dumps(result)



api.add_resource(WithinDistance, '/withindist/')
api.add_resource(BBox, '/boundingbox/')
api.add_resource(GetTile,'/tiledatatemp/')
api.add_resource(GetBox, '/boundingboxtemp/')
api.add_resource(Tile, '/tiledata')

if __name__ == '__main__':
    app.run(debug=True)